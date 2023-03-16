#!/usr/bin/env python3
"""
session auth
"""
from os import getenv
from typing import TypeVar
from uuid import uuid4

from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    """
    Session auth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        sid = str(uuid4())
        self.user_id_by_session_id[sid] = user_id

        return sid

    def user_id_for_session_id(self, sid: str = None) -> str:
        """gets user_id in a session"""
        if sid is None or not isinstance(sid, str):
            return None

        return self.user_id_by_session_id.get(sid, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """fetches the current user with sid"""
        if request is None:
            return None
        sid = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sid)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes a session"""
        if request is None:
            return False

        sid = self.session_cookie(request)
        if sid is None:
            return False
        if self.user_id_for_session_id(sid) is None:
            return False

        del self.user_id_by_session_id[sid]
        return True
