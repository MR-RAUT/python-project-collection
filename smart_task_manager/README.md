# 🚀 Smart Task Manager – Full Stack Flask Application

A **production-style, full-stack web application** built using **Flask** that enables users to securely manage tasks with a clean UI and scalable backend architecture.

This project demonstrates **real-world backend development practices**, including authentication, database relationships, modular design, and UI integration.

---

## 📌 Why This Project Matters

✔ Built using **Flask App Factory Pattern**  
✔ Modular architecture with **Blueprints**  
✔ Secure authentication system  
✔ Clean UI with Bootstrap  
✔ Database migrations & ORM usage  
✔ Recruiter-ready codebase  

> This project is designed to reflect how **real software is built in companies**, not just a demo app.

---

## ✨ Features

### 🔐 Authentication & Security
- User registration & login
- Secure password hashing using **Flask-Bcrypt**
- Session management with **Flask-Login**
- Route protection using `@login_required`

### 🗂 Task Management
- Add new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed
- User-specific task isolation

### 🎨 UI & UX
- Modern responsive design using **Bootstrap 5**
- Template inheritance using `base.html`
- Toast notifications for dashboard
- Inline alerts for login & registration
- Clean, professional layout

### 🛠 Engineering Practices
- Flask Blueprints for modular code
- SQLAlchemy ORM with relationships
- Database migrations using Flask-Migrate
- Unit testing support
- Clean folder structure

---

## 🧰 Tech Stack

### Backend
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-Migrate

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (ES6)

### Database
- SQLite (development)
- Easily extendable to PostgreSQL / MySQL

---

## 📁 Project Structure

```text
smart_task_manager/
│
├── app/
│   ├── __init__.py          # App factory
│   ├── extensions.py       # DB, LoginManager, Bcrypt
│   │
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── task.py          # Task model
│   │
│   ├── auth/                # Authentication module
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── tasks/               # Task management module
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
│   │   └── js/
│   │
│   └── config.py
│
├── migrations/              # Database migrations
├── tests/                   # Unit tests
├── requirements.txt
├── run.py
└── README.md


Perfect 👍
Below is a **clean, recruiter-friendly “Installation & Setup” section** that you can **directly paste into your README.md**.
It includes **all correct steps**, avoids confusion, and matches your Flask App Factory + Migrations setup.

---

## ⚙️ Installation & Setup

Follow the steps below to run **Smart Task Manager** locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/smart_task_manager.git
cd smart_task_manager
```

---

### 2️⃣ Create & Activate Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Flask Environment Variables

#### Windows (PowerShell)

```bash
$env:FLASK_APP="run.py"
$env:FLASK_ENV="development"
```

#### macOS / Linux

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

---

### 5️⃣ Initialize Database & Migrations (First Time Only)

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

> ⚠️ Skip `flask db init` if the `migrations/` folder already exists.

---

### 6️⃣ Run the Application

```bash
python run.py
```

---

### 7️⃣ Access the Application

Open your browser and visit:

```
http://127.0.0.1:----
```

---

## 🧪 (Optional) Run Tests

```bash
pytest
```

---

## 🔑 Default Workflow

1. Register a new account
2. Login securely
3. Add, edit, complete, or delete tasks
4. View tasks on dashboard

---

## ✅ Notes for Recruiters

* Uses Flask App Factory Pattern
* Database handled via SQLAlchemy ORM
* Secure authentication using Flask-Login & Bcrypt
* Modular, scalable folder structure

---
