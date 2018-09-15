"""Collection of helper functions."""

import os


def get_env_var(var_name):
    """Return env var or print exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f'Set the {var_name} environment variable.'
        print(error_msg)
