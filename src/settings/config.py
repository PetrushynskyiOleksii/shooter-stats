"""The configurations for a project."""

from .utils import get_env_var


class BaseConfig(object):
    """Parent configuration class."""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = get_env_var('SECRET')
    SQLALCHEMY_DATABASE_URI = get_env_var('DATABASE_URL')


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
