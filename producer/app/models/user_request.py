"""
Module contains User Requests model definition and helper functions for manipulating with it.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import select
from app.models import Base


class UserRequests(Base):
    """
    User requests model class.
    """
    __tablename__ = 'user_requests'

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    git_client = Column(String(16))
    version = Column(String(16))
    repo = Column(String(128))
    owner = Column(String(64))
    token = Column(String(128))
    hash = Column(String(128))
    branch = Column(String(128))
    action = Column(String(32))
    user_id = Column(Integer)

def get_user_requests(user):
    """Get user requests for registered user"""
    sel = select(['user_requests'])
    print(sel)
    return sel
