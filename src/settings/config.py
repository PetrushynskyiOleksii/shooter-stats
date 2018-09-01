"""The configurations for a project."""

import os


class BaseConfig(object):
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET', 'default_secret_key')


class DevelopmentConfig(BaseConfig):
    """Configurations for Development."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Configurations for Production."""

    DEBUG = False
    TESTING = False


# TODO: testing config

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
