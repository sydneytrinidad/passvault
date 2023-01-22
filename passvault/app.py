from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Application Configuration
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db" #TODO:Env var this

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Create Database Models
        db.create_all()
        session = Session(app)
        return app