#!/usr/bin/env python3
"""
filters and obfuscate fields from a message
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, sep: str) -> str:
    """
    uses regex to identify and
    redact specified fields from message
    :param fields: list of fields to be redacted
    :param redaction: string to replace the redacted
                        field's value with
    :param message: str that contain the fields and values
    :param sep: separator char the delineate field-value pairs
                in message

    :return: message with fields in fields param redacted
    """
    for field in fields:
        # matches one or more char that is not the 'sep'
        # and preceded by 'field=' and followed by 'sep'
        regex: str = f'(?<={field}=)([^{sep}]+)(?={sep})'
        message: str = re.sub(regex, redaction, message)
    return message
