from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config_options

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'Strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
