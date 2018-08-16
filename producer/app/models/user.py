from sqlalchemy import Column, String, Integer
from app.models import Base


class User(Base):
    __tablename__ = 'user'

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))


    # Methods
    def __repr__(self):
        """ Show user object info. """
        return '<User: {}>'.format(self.id)
