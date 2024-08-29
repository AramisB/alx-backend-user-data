#!/usr/bin/env python3
"""
A module for logging personal data
"""
import logging
import re
import os
import mysql.connector
from typing import List
import bcrypt


# Constants
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message with specified fields obfuscated
    """
    return re.sub(
        f"({'|'.join(fields)})=[^{separator}]*",
        lambda match: f"{match.group().split('=')[0]}={redaction}", message
        )


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the Redacting Formatter with specific fields
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with sensitive fields obfuscated
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger with specific settings
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the secure database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def log_user_data():
    """
    Logs user data from the database
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for (name, email, phone, ssn, password,
         ip, last_login, user_agent) in cursor:
        message = (
            f"name={name}; email={email}; phone={phone}; ssn={ssn}; "
            f"password={password}; ip={ip}; last_login={last_login}; "
            f"user_agent={user_agent};"
            )
        logger.info(message)

    cursor.close()
    db.close()


def hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt and returns the salted,
    hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


if __name__ == "__main__":
    log_user_data()
