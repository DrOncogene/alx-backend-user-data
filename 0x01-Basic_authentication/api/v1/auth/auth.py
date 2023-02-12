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
        return False

    def authorization_header(self, request=None) -> str:
        """
        gets the authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """fetches the current user"""
        return None