Excellent 👍
You shared a **high-quality README template** for NovaDhi — I’ll now create a **same-level, professional, ATS-friendly, portfolio-ready README** for your:

# 🧠 Smart Task Manager (Flask Project)

You can directly copy–paste this into your `README.md`.

---

# 🧠 Smart Task Manager – Flask Web Application

Smart Task Manager is a **full-stack Flask-based web application** that helps users efficiently manage their daily tasks with secure authentication, user-specific task tracking, and a clean dashboard interface.

The system follows an **industry-standard Flask blueprint architecture** and implements secure login, task CRUD operations, and database-backed persistence using SQLAlchemy.

This project demonstrates practical knowledge of **Python backend development, Flask framework, authentication, relational databases, and MVC-style design**.

---

## 📌 Key Highlights

* User authentication (Register / Login / Logout)
* Secure password hashing using Bcrypt
* User-specific task management
* Add, Edit, Delete, and View tasks
* Priority and due date support
* Flask Blueprint modular architecture
* SQLite database with SQLAlchemy ORM
* Clean and responsive UI

---

## 🖼 Screenshots

Example:

### Login Page

![Login](screenshots/login.png)

### Register Page

![Register](screenshots/register.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Add Task

![Add Task](screenshots/add_task.png)

---

## 🎯 Why Smart Task Manager?

Managing tasks using notes or spreadsheets becomes messy and inefficient. Smart Task Manager provides a centralized, secure, and easy-to-use platform where users can:

* Track personal tasks
* Set priorities
* View all tasks in one dashboard
* Edit or delete tasks anytime
* Keep data isolated per user

It is ideal for:

* Students
* Developers
* Professionals
* Beginners learning Flask

---

## 🧩 Features in Detail

### 1. Authentication System

* User registration
* Secure login/logout
* Password hashing using Bcrypt
* Flask-Login session management

### 2. Task Management

* Create new tasks
* Edit existing tasks
* Delete tasks
* View all tasks on dashboard

### 3. User Isolation

* Each user sees only their own tasks
* Foreign key mapping between users and tasks

### 4. Database Layer

* SQLite database
* SQLAlchemy ORM
* Flask-Migrate ready

### 5. Modular Architecture

* Separate blueprints for authentication and tasks
* Clean separation of concerns

---

## 🏗 Project Structure

```
smart_task_manager/
│
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py       # DB, login, bcrypt
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   │
│   ├── auth/                # Authentication module
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── tasks/               # Task management module
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── tasks/
│   │   │   ├── dashboard.html
│   │   │   ├── add_task.html
│   │   │   └── edit_task.html
│   │   └── base.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── bootstrap/
│   │
│   └── config.py
├── screenshots/
├── migrations/              # Database migrations
├── tests/
│   └── test_tasks.py
│
├── requirements.txt
├── run.py
└── README.md
```

---

## 🛠 Tech Stack

* Python 3.10+
* Flask
* Flask-Login
* Flask-WTF
* Flask-Bcrypt
* Flask-SQLAlchemy
* SQLite
* HTML5 / CSS3 / Bootstrap

---

## ⚙️ Installation Guide

### Step 1: Clone Repository

```
git clone https://github.com/MR-RAUT/python-project-collection.git
cd python-project-collection/smart_task_manager
```

### Step 2: Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

### Step 4: Initialize Database

```
flask shell
```

```python
from app import create_app
from app.extensions import db
app = create_app()
app.app_context().push()
db.create_all()
exit()
```

---

## ▶️ Run Application

```
python run.py
```

Open browser:

```
http://127.0.0.1:5000/auth/login
```

---

## 🔐 Default Flow

1. Register new account
2. Login
3. Access Dashboard
4. Add / Edit / Delete tasks

---

## 🧪 Testing

```
pytest
```

---

## 🔒 Security

* Passwords are hashed
* CSRF protection via Flask-WTF
* User session management with Flask-Login

---

## 🚀 Future Enhancements

* Task status (Pending / Completed)
* Search and filters
* REST API version
* Pagination
* Email verification
* Deployment on AWS / Render

---

## 👨‍💻 Author

**Mahesh Raut**
B.Tech Artificial Intelligence & Data Science

---

## ⭐ Support

If you found this project helpful, consider giving it a star ⭐ on GitHub.

---

