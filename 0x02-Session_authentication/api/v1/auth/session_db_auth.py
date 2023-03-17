#!/usr/bin/env python3
"""
session login with db
"""
from datetime import datetime
from uuid import uuid4

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """session login with db"""
    def create_session(self, user_id: str = None) -> str:
        """creates a new UserSession"""
        if user_id is None:
            return None

        sid = str(uuid4())
        new_session = UserSession(user_id=user_id, session_id=sid)
        new_session.save()
        self.user_id_by_session_id[sid] = {
            'session': new_session,
            'created_at': datetime.now()
        }

        return new_session.session_id

    def user_id_for_session_id(self, sid: str = None) -> str:
        """fetches user data from session"""
        if sid is None or not isinstance(sid, str):
            return None

        sess = UserSession.search({'session_id': sid})
        if len(sess) == 0:
            return None
        
        session_dict = self.user_id_by_session_id[sid]
        if not session_dict.get('created_at', None):
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id', None)

        created = session_dict['created_at'].timestamp()
        if datetime.now().timestamp() > created + self.session_duration:
            return None

        return sess[0].user_id

    def destroy_session(self, request=None):
        if request is None:
            return False

        sid = self.session_cookie(request)
        if sid is None:
            return False

        sess = UserSession.search({'session_id': sid})
        if len(sess) == 0:
            return False

        sess[0].remove()
        return True
