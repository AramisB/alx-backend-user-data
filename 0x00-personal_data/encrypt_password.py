#!/usr/bin/env python3
"""
Module to encrypt password
"""
import bcrypt
from filtered_logger import hash_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password
    args: hashed_password: bytes type
          password: string type
    Return: True if the password matches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
