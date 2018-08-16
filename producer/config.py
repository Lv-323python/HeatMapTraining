import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ...
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    AUTH_LOGIN_ENDPOINT = 'login'