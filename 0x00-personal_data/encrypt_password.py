#!/usr/bin/env python3
"""
hashing and encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashes passwords"""
    salt = bcrypt.gensalt()
    password = password.encode('utf-8')

    return bcrypt.hashpw(password, salt=salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """verifies a password"""
    password = password.encode('utf-8')
    valid = bcrypt.checkpw(password, hashed_password)

    return valid
