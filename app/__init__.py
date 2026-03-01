from flask import Flask
from app.teachers.route import teachers_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret123"

    app.register_blueprint(teachers_bp)

    return app