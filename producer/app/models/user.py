from sqlalchemy import Column, String, Integer
from app.models import Base
from app import auth
from app.database import scoped_session
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'user'

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))


    # Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """ Show user object info. """
        return '<User: id={}, username={}>'.format(self.id, self.username)


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
        with scoped_session() as session:
            return session.query(User).filter_by(username=token['username']).first()

def get_user_by_name(name):
    with scoped_session() as session:
        return session.query(User).filter_by(username=name).first()