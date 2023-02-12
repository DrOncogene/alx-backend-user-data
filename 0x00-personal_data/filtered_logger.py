#!/usr/bin/env python3
"""
filters and obfuscate fields from a message
"""
import os
import re
import logging
from typing import List
from mysql.connector.connection import MySQLConnection
from mysql import connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    uses regex to identify and
    redact specified fields from message
    """
    for field in fields:
        # matches one or more char that is not the 'sep'
        # and preceded by 'field=' and followed by 'sep'
        regex = f'(?<={field}=)([^{separator}]+)(?={separator})'
        message = re.sub(regex, redaction, message)

    return message


def get_logger() -> logging.Logger:
    """
    creates and returns a logger
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    creates and return a connection object
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db = connector.connect(user=user, password=passwd,
                           host=host, database=db_name)

    return db


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """constructor"""
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        uses filter_datum to redact the record
        msg and formats it
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        message = super().format(record)
        return message


def main():
    """
    creates a logger, connects to
    the database and logs the result
    """
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    for user in cursor:
        msg = (
            f"name={user[0]}; email={user[1]}; phone={user[2]}; "
            f"ssn={user[3]}; password={user[4]}; ip={user[5]}; "
            f"last_login={user[6]}; user_agent={user[7]};"
        )

        logger.info(msg)


if __name__ == "__main__":
    main()
