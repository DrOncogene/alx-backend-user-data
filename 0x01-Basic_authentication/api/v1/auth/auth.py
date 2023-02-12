#!/usr/bin/env python3
"""
the auth module
"""
from typing import List, TypeVar
import requests


class Auth:
    """
    the auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if path require auth
        """
        if path is None or excluded_paths is None:
            return True

        if path[-1] != '/':
            path_2 = path + '/'
        else:
            path_2 = path[:-2]

        if path not in excluded_paths and path_2 not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
        gets the authorization header
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """fetches the current user"""
        return None
