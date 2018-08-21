import os
from postgres_helpers.postgres_config import HOST, PORT, POSTGRES_USER, POSTGRES_PASSWORD, HEAT_MAP_DB

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ...
    DATABASE_URL = os.environ.get('DATABASE_URL') or f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{HOST}:{PORT}/{HEAT_MAP_DB}'# 'sqlite:///' + os.path.join(basedir, 'app.db')
    AUTH_LOGIN_ENDPOINT = 'login'