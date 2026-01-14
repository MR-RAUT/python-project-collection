from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.tasks.forms import TaskForm
from app.models.task import Task
from app.extensions import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Dashboard
@tasks_bp.route("/")
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("tasks/dashboard.html", tasks=tasks)

# Add Task
@tasks_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data,
                    description=form.description.data,  
                    due_date=form.due_date.data, 
                    priority=form.priority.data,
                    user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Task added successfully!", "success")
        return redirect(url_for("tasks.dashboard"))
    return render_template("tasks/add_task.html", form=form)

# Edit Task
@tasks_bp.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data  
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("tasks.dashboard"))
    return render_template("tasks/edit_task.html", form=form, task=task)

# Delete Task
@tasks_bp.route("/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "danger")
    return redirect(url_for("tasks.dashboard"))

# Mark complete
@tasks_bp.route("/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Completed"
    db.session.commit()
    flash("Task marked as completed!", "success")
    return redirect(url_for("tasks.dashboard"))
