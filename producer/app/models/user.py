"""
Module contains User model definition and helper functions for manipulating with it.
"""

from sqlalchemy import Column, String, Integer
from app.models import Base
from app import auth
from app.database import scoped_session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    """
    User model class.
    """
    __tablename__ = 'user'

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    # Methods
    def set_password(self, password):
        """Set user password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check user password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """ Show user object info. """
        return '<User: id={}, username={}>'.format(self.id, self.username)


def get_user_by_name(username):
    """
    Validate user username

    Returns None if there is no record  in the database with the specified username, else User object

    :param username: string
    :return: User object or None
    """
    with scoped_session() as session:
        return session.query(User).filter_by(username=username).first()


def get_user_by_email(email):
    """
    Validate user email

    Returns None if there is no record  in the database with the specified email, else User object

    :param email: string
    :return: User object or None
    """
    with scoped_session() as session:
        return session.query(User).filter_by(email=email).first()


def register_user(username, email, password):
    """
    Register the user, stores user record in a database

    :param username: string
    :param email: string
    :param password: string
    """
    with scoped_session() as session:
        user = User(username=username, email=email)
        user.set_password(password)
        session.add(user)


@auth.serializer
def serialize(user):
    """Serialize the user, returns a token to be placed into session"""
    return {
        'uid': user.id,
        'username': user.username
    }


@auth.user_loader
def load_user(token):
    """Load user with token.

    Return a User object
    """
    if token is not None:
        return get_user_by_name(token['username'])
