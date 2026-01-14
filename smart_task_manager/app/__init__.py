from flask import Flask, redirect, url_for
from .config import Config
from .extensions import db, login_manager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Import and register blueprints
    from .auth.routes import auth_bp
    from .tasks.routes import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Root route redirect
    @app.route("/")
    def home():
        return redirect(url_for("tasks.dashboard"))

    return app
