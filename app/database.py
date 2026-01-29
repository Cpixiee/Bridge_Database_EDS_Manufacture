from typing import Generator

import mysql.connector
from mysql.connector import MySQLConnection

from .config import get_settings


def get_db_connection() -> MySQLConnection:
    """
    Membuat koneksi baru ke database MySQL.
    Caller bertanggung jawab menutup koneksi setelah selesai.
    """
    settings = get_settings()

    connection = mysql.connector.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
    )
    return connection


def get_db() -> Generator[MySQLConnection, None, None]:
    """
    Dependency FastAPI untuk menyediakan koneksi DB per-request.
    """
    connection: MySQLConnection | None = None
    try:
        connection = get_db_connection()
        yield connection
    finally:
        if connection and connection.is_connected():
            connection.close()


