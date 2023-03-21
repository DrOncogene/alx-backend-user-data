#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    hashes a string
    """
    salt = gensalt()
    hashed = hashpw(password.encode('utf-8'), salt)

    return hashed
