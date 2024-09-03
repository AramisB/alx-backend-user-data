#!/usr/bin/env python3
"""
A module for API auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns false
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns none
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
