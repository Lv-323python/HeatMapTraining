""" This module exports the database engine.

Notes:
     Using the scoped_session contextmanager is
     best practice to ensure the session gets closed
     and reduces noise in code by not having to manually
     commit or rollback the db if a exception occurs.
"""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app

DATABASE_URL = app.config['DATABASE_URL']
ENGINE = create_engine(DATABASE_URL)

# Session to be used throughout app.
SESSION = sessionmaker(bind=ENGINE)


@contextmanager
def scoped_session():
    session = SESSION()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
