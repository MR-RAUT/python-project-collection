import os

class Config:
    SECRET_KEY = "this-is-a-secret-key"  # Change this in production
    SQLALCHEMY_DATABASE_URI = "sqlite:///smart_tasks.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
