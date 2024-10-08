#!/usr/bin/env python3
"""
Module qith class BasicAuth
"""

from api.v1.auth.auth import Auth
import base64
from typing import TypeVar

User = TypeVar('User')


class BasicAuth(Auth):
    """
    Inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication:
        Return None if authorization_header is None
        Return None if authorization_header is not a string
        Return None if authorization_header doesn’t start
        by Basic (with a space at the end)
        Otherwise, return the value after Basic (after the space)
        You can assume authorization_header contains only one Basic
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ", 1)[1]


    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str: 
        """
        returns the decoded value of a Base64 string base64_authorization_header:
        Return None if base64_authorization_header is None
        Return None if base64_authorization_header is not a string
        Return None if base64_authorization_header
        is not a valid Base64 - you can use try/except
        Otherwise, return the decoded value as UTF8 string
        you can use decode('utf-8')
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        Return None, None if decoded_base64_authorization_header is None
        Return None, None if decoded_base64_authorization_header is not a string
        Return None, None if decoded_base64_authorization_header doesn’t contain :
        Otherwise, return the user email and password
        - these 2 values must be separated by a :
        You can assume decoded_base64_authorization_header will contain only one :
        """
        if (decoded_base64_authorization_header is None or
            not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        # Find the first occurrence of ':' to split user email and password
        separator_index = decoded_base64_authorization_header.find(':')
        if separator_index == -1:
            return None, None

        # Split into email and password based on the first colon found
        email = decoded_base64_authorization_header[:separator_index]
        password = decoded_base64_authorization_header[separator_index + 1:]

        return email, password

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on user_email and user_pwd.
        Return None if user_email or user_pwd is None or not a string
        Return None if no User instance is found with the given email
        Return None if user_pwd is not valid for the User instance
        Otherwise, return the User instance
        """
        if (user_email is None or not isinstance(user_email, str)
            or user_pwd is None or not isinstance(user_pwd, str)):
            return None

        users = User.search(email=user_email)
        if not users:
            return None

        user = users[0]  # Assuming unique email, take the first result

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on user_email and user_pwd.
        Return None if user_email or user_pwd is None or not a string
        Return None if no User instance is found with the given email
        Return None if user_pwd is not valid for the User instance
        Otherwise, return the User instance
        """
        if (user_email is None or not isinstance(user_email, str) or
            user_pwd is None or not isinstance(user_pwd, str)):
            return None

        # Assuming User class has a method `search` that returns a list of users
        users = User.search(email=user_email)
        if not users:
            return None
        
        user = users[0]  # Assuming unique email, take the first result

        if not user.is_valid_password(user_pwd):
            return None
        
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        Uses authorization_header
        Uses extract_base64_authorization_header
        Uses decode_base64_authorization_header
        Uses extract_user_credentials
        Uses user_object_from_credentials
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if base64_auth_header is None:
            return None
        
        decoded_auth_header = self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth_header is None:
            return None
        
        email, password = self.extract_user_credentials(decoded_auth_header)
        if email is None or password is None:
            return None
        
        return self.user_object_from_credentials(email, password)
