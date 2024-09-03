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
            # Normalize the excluded_pathgit 
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            # Check if the path starts with the excluded path
            if path.startswith(excluded_path):
                return False
        return True

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
