#!/usr/bin/env python3
"""
A module for personal sensitive data obfuscation.
"""
import re
import logging


def filter_datum(fields, redaction, message, separator):
    """
    args: fields: a list of strings representing all fields to obfuscate
         redaction: a string representing by what the field will be obfuscated
         message: a string representing the log line
         separator: a string representing
         by which character is separating all fields in the log line
    Returns: the log line obfuscated
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator, field + "="
                         + redaction + separator, message)
    return message
