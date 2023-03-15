#!/usr/bin/env python3
"""
session auth
"""
from uuid import uuid4

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
