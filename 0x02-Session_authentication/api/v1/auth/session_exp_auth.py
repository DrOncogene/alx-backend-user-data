#!/usr/bin/env python3
"""
session login with expiration
"""
from os import getenv
from datetime import datetime

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """expiring session auth class"""
    def __init__(self) -> None:
        self.session_duration = int(getenv('SESSION_DURATION') or 0)
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """creates a session"""
        sid = super().create_session(user_id)
        if sid is None:
            return None

        self.user_id_by_session_id[sid] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return sid

    def user_id_for_session_id(self, sid: str = None) -> str:
        """fetches user data from session"""
        if sid is None:
            return None
        if not self.user_id_by_session_id.get(sid, None):
            return None

        session_dict = self.user_id_by_session_id[sid]
        if not session_dict.get('created_at', None):
            return None

        created = session_dict['created_at'].timestamp()
        if datetime.now().timestamp() > created + self.session_duration:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id', None)

        return session_dict['user_id']
