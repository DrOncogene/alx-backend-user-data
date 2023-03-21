#!/usr/bin/env python3
"""
auth module
"""
from sqlalchemy.exc import NoResultFound
from bcrypt import hashpw, gensalt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    hashes a string
    """
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)

    return hashed


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
