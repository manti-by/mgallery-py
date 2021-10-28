import sqlite3
from typing import Awaitable

from mgallery.settings import DATABASE_PATH


def dict_factory(cursor: sqlite3.Cursor, row: dict) -> dict:
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


async def list_images() -> Awaitable[list]:
    with sqlite3.connect(DATABASE_PATH) as session:
        session.row_factory = dict_factory
        cursor = session.cursor()
        cursor.execute("SELECT * FROM image")
        session.commit()
        return cursor.fetchall()


async def get_duplicates(exclude: list = None) -> Awaitable[list]:
    with sqlite3.connect(DATABASE_PATH) as session:
        session.row_factory = dict_factory
        cursor = session.cursor()
        cursor.execute(
            f"""
            SELECT a.*
            FROM image a
            JOIN (
              SELECT phash, COUNT(*)
              FROM image
              WHERE name NOT IN ('{"','".join(exclude)}')
              GROUP BY phash
              HAVING COUNT(*) > 1
            ) b ON a.phash = b.phash
            ORDER BY a.phash;
        """
        )
        session.commit()
        return cursor.fetchall()


async def create_image(
    path: str,
    name: str = None,
    phash: str = None,
    size: int = None,
    width: int = None,
    height: int = None,
) -> Awaitable[int]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO image (path, name, phash, size, width, height) VALUES (?, ?, ?, ?, ?, ?)",
            (path, name, phash, size, width, height),
        )
        connection.commit()
        return cursor.lastrowid
