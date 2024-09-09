#!/usr/bin/env python3
"""
__hash_password method
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes the given password using bcrypt
    and returns the salted hash as bytes.
    Args:
        password (str): The plain-text password to hash.
    Returns:
       bytes: The salted and hashed password.
    """
    password_bytes = password.encode('utf-8')

    hashed_pwd = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_pwd
