#!/usr/bin/env python3
"""
A module for API auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    A class that defines routes that require authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns false
        Returns True if path is None
        Returns True if excluded_paths is None or empty
        Returns False if path is in excluded_paths
        assume excluded_paths contains string path always ending by a /
        This method must be slash tolerant:
        path=/api/v1/status and path=/api/v1/status/
        must be returned False if excluded_paths contains /api/v1/status/
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Normalize the excluded path
            if excluded_path.endswith('*'):
                # Check if the path matches the prefix before the '*'
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                # Match exact path with trailing slash normalization
                if path == excluded_path or path + '/' == excluded_path:
                    return False

        return True
    def authorization_header(self, request=None) -> str:
        """
        Returns none
        If request is None, returns None
        If request doesn’t contain the header key Authorization, returns None
        Otherwise, return the value of the header request Authorization
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
