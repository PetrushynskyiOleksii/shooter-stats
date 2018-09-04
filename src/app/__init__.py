"""The app configuration module."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import app_config


db = SQLAlchemy()


def create_app(config_name):
    """Create FlaskAPI application."""
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views.shooter import shooter_api
    app.register_blueprint(shooter_api, url_prefix='/servers')

    from .views.players import players_api
    app.register_blueprint(players_api, url_prefix='/players')

    return app


from .models import players, shooter
