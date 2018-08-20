"""
This is a config module for producer
"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    This is a config class for producer
    """
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    AUTH_LOGIN_ENDPOINT = 'login'
