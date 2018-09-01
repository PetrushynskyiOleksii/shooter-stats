"""The app configuration module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import app_config


def create_app(config_name):
    """Create FlaskAPI application."""
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize db
    db = SQLAlchemy()
    db.init_app(app)

    return app
