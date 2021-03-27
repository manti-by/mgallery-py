import sqlite3

from mgallery.settings import DATABASE_PATH


def dict_factory(cursor: sqlite3.Cursor, row: dict) -> dict:
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class GalleryService:
    @staticmethod
    def get(gallery_id: int) -> dict:
        with sqlite3.connect(DATABASE_PATH) as session:
            session.row_factory = dict_factory
            cursor = session.cursor()
            cursor.execute("SELECT * FROM gallery WHERE id = ?", (gallery_id,))
            session.commit()
            return cursor.fetchone()

    @staticmethod
    def list() -> list:
        with sqlite3.connect(DATABASE_PATH) as session:
            session.row_factory = dict_factory
            cursor = session.cursor()
            cursor.execute("SELECT * FROM gallery")
            session.commit()
            return cursor.fetchall()

    @staticmethod
    def create(path: str, name: str = None) -> int:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO gallery (path, name) VALUES (?, ?)", (path, name)
            )
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def delete(gallery_id: int):
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM gallery WHERE id = ?", (gallery_id,))
            connection.commit()


class ImageService:
    @staticmethod
    def get(image_id: int) -> dict:
        with sqlite3.connect(DATABASE_PATH) as session:
            session.row_factory = dict_factory
            cursor = session.cursor()
            cursor.execute("SELECT * FROM image WHERE id = ?", (image_id,))
            session.commit()
            return cursor.fetchone()

    @staticmethod
    def list(gallery_id: int = None, exclude: list = None) -> list:
        with sqlite3.connect(DATABASE_PATH) as session:
            session.row_factory = dict_factory
            cursor = session.cursor()
            query = "SELECT * FROM image"
            if gallery_id is not None:
                query += f" WHERE gallery_id = {gallery_id}"
                if exclude is not None:
                    query += f" AND id NOT IN ({','.join(map(str, exclude))})"
            elif exclude is not None:
                query += f" WHERE id NOT IN ({','.join(map(str, exclude))})"
            cursor.execute(query)
            session.commit()
            return cursor.fetchall()

    @staticmethod
    def create(
        gallery_id: int,
        path: str,
        name: str = None,
        phash: str = None,
        size: int = None,
        width: int = None,
        height: int = None,
    ) -> int:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO image (path, name, phash, size, width, height, gallery_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (path, name, phash, size, width, height, gallery_id),
            )
            connection.commit()
            return cursor.lastrowid

    @staticmethod
    def update(
        image_id: int,
        phash: str = None,
        size: int = None,
        width: int = None,
        height: int = None,
    ):
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE image SET phash = ?, size = ?, width = ?, height = ? WHERE id = ?",
                (phash, size, width, height, image_id),
            )
            connection.commit()

    @staticmethod
    def delete(image_id: int):
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM image WHERE id = ?", (image_id,))
            connection.commit()
