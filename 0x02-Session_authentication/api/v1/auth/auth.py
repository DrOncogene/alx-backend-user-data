#!/usr/bin/env python3
"""
the auth module
"""
from os import getenv

from typing import List, TypeVar
import re


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

        exists = False
        for item in excluded_paths:
            exists = re.match(item, path) or re.match(item, path_2)
            if exists:
                return False

        return True

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

    def session_cookie(self, request=None):
        """gets the cookies"""
        if request is None:
            return None

        SESSION_NAME = getenv('SESSION_NAME') or '_my_session_id'
        return request.cookies.get(SESSION_NAME, None)
