""" This module exports the database engine.

Notes:
     Using the scoped_session contextmanager is
     best practice to ensure the session gets closed
     and reduces noise in code by not having to manually
     commit or rollback the db if a exception occurs.
"""
import os
import time
from alembic import command
from alembic.config import Config
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, OperationalError as SQLAlchemyConnectionError
from app import app


from app.db_connection import create_database

print('waiting 30 seconds')
time.sleep(30)
create_database()

DATABASE_URL = app.config['DATABASE_URL']

ALEMBIC_INI_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'alembic.ini')
ALEMBIC_CFG = Config(ALEMBIC_INI_FILE)
command.upgrade(ALEMBIC_CFG, "head")

ENGINE = create_engine(DATABASE_URL)
# Session to be used throughout app.
SESSION = sessionmaker(bind=ENGINE, expire_on_commit=False)


while True:
    try:
        # declare connection
        CONNECTION = ENGINE.connect()
        break
    except SQLAlchemyConnectionError as exc:
        if RETRIES == 0:
            print('Failed to connect!')
            raise exc
        RETRIES -= 1
        time.sleep(1)
print('Successfully connected!')
CONNECTION.close()




@contextmanager
def scoped_session():
    session = SESSION()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close()
