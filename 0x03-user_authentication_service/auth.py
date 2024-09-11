#!/usr/bin/env python3
"""
Module for Authentication
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import uuid
from user import User


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

    def register_user(self, email: str, password: str) -> 'User':
        """
        Registexr a new user with the given email and password.
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
            new_user = self._db.add_user(email, hashed_password)
            return new_user

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

    def _generate_uuid(self) -> str:
        """
        return a string representation of a new UUID
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        Finds the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id, then return the session ID.
        args: email (str) - the email of the user
        Returns: the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Find the user corresponding to the session ID
        Args:
        session_id string argument
        Returns:the corresponding User or None.
        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        The method takes a single user_id integer argument
        and returns None.
        The method updates the corresponding user’s session ID to None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset_token for a password to a specifies user email
        Args: email -> str: users email
        Returns: generated token as a string.
        Find the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID
        and update the user’s reset_token database field.
        """
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Args:
          reset_token: str - the reset token
          password: str - the new password
        Returns: None.
        Use the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception.
        Otherwise, hash the password
        and update the user’s hashed_password field
        with the new hashed password
        and the reset_token field to None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            return self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
                )
        except NoResultFound:
            raise ValueError
