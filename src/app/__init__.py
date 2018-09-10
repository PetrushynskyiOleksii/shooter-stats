"""The app configuration module."""

import connexion
from flask_sqlalchemy import SQLAlchemy

from settings import app_config


db = SQLAlchemy()


def create_app(config_name):
    """Create FlaskAPI application."""
    app = connexion.App(__name__)
    app.add_api('swagger.yml')
    application = app.app

    application.config.from_object(app_config[config_name])
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(application)

    return application


from .models import *
