#!/usr/bin/env python3
"""
User module
"""

from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    User class
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """
        String representation of User
        """
        return "<User id={self.id} email={self.email}>".format(self=self)
