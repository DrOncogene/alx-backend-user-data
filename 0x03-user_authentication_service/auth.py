#!/usr/bin/env python3
"""
auth module
"""
from typing import Optional
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a string
    """
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)

    return hashed


def _generate_uuid() -> str:
    """
    generates random uuids
    """
    return str(uuid4())


class Auth:
    """Auth class"""
    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        adds a new user
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            pass

        passwd = _hash_password(password)

        return self._db.add_user(email, passwd)

    def valid_login(self, email: str, password: str) -> bool:
        """
        validates the user password
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        generates new sessions
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        fetches a user from session_id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
