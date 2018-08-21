"""
This is a config module for producer
"""
import os
from postgres_helpers.postgres_config import HOST, PORT, POSTGRES_USER, POSTGRES_PASSWORD, HEAT_MAP_DB

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ...
    """
    This is a config class for producer
    """
    DATABASE_URL = os.environ.get(
        'DATABASE_URL') or f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{HEAT_MAP_DB}'
    AUTH_LOGIN_ENDPOINT = 'login'
