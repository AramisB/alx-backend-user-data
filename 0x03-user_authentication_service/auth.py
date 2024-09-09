#!/usr/bin/env python3
"""
Module for Authentication
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt
    and returns the salted hash as bytes.
    Args:
        password (str): The plain-text password to hash.
    Returns:
       bytes: The salted and hashed password.
    """
    password_bytes = password.encode('utf-8')

    hashed_pwd = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_pwd


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> None:
        """
        Register a new user with the given email and password.
        Args:
         email - the email of the user
         password - the password of the user
        Raises:
         ValueError - if the user already exists
         with message User <user's email> already exists.
        If not, hash the password with _hash_password,
        save the user to the database using self._db
        and return the User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            self._db.add_user(email, hashed_password)
            return self._db.find_user_by(email=email)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the given email and password are valid.
        Args:
         email - the email of the user
         password - the password of the user
        If email exists, check the password with bcrypt.checkpw.
        If it matches return True, else return False
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False
