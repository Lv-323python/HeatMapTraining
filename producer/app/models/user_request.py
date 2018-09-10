"""
Module contains User Requests model definition and helper functions for manipulating with it.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import select
from app.models import Base
from app.database import scoped_session


class UserRequests(Base):
    """
    User requests model class.
    """
    __tablename__ = 'user_requests'

    # Attributes
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)
    git_client = Column(String(16))
    version = Column(String(16))
    repo = Column(String(128))
    owner = Column(String(64))
    token = Column(String(128))
    hash = Column(String(128))
    branch = Column(String(128))
    action = Column(String(32))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'git_client': self.git_client,
            'version': self.version,
            'repo': self.repo,
            'owner': self.owner,
            'token': self.token,
            'hash': self.hash,
            'branch': self.branch,
            'action': self.action

        }


def save_repo_info(body):
    """Save user requests for registered user"""
    with scoped_session() as session:
        user_id = int(body.get('user_id'))
        git_client = str(body.get('git_client'))
        version = body.get('version')
        repo = body.get('repo')
        owner = body.get('owner')
        token = body.get('token')
        hash = body.get('hash')
        branch = body.get('branch')
        action = body.get('action')
        user_requsts = UserRequests(user_id=user_id, git_client=git_client, version=version,
                                    repo=repo, owner=owner, token=token, hash=hash, branch=branch,
                                    action=action)
        session.add(user_requsts)


def get_repo_info_row(id):
    """Get user repo info for registered user"""
    with scoped_session() as session:
        return session.query(UserRequests).filter_by(id=id).first()


def get_repo_info(user_id):
    """Get user repo info for registered user"""
    with scoped_session() as session:
        return session.query(UserRequests).filter_by(user_id=user_id).\
            order_by(UserRequests.id.asc())


def delete_repo_info(id):
    """Delete user repo info for registered user"""
    with scoped_session() as session:
        return session.query(UserRequests).filter_by(id=id).delete()


def update_repo_info(id, body):
    """Update user repo info for registered user"""
    with scoped_session() as session:
        git_client = str(body.get('git_client'))
        version = body.get('version')
        repo = body.get('repo')
        owner = body.get('owner')
        token = body.get('token')
        hash = body.get('hash')
        branch = body.get('branch')
        action = body.get('action')
        return session.query(UserRequests).filter_by(id=id).update({'git_client': git_client,
                                                                    'version': version,
                                                                    'repo': repo, 'owner': owner,
                                                                    'token': token, 'hash': hash,
                                                                    'branch': branch,
                                                                    'action': action, })
