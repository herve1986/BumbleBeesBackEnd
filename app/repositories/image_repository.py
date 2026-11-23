
from app.models.image import Image


class ImageRepository:

    def __init__(self, db):
        self.db = db

    def create(self, image: Image) -> Image:
        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO images (title, url)
            VALUES (?, ?)
            """,
            (image.title, image.url)
        )

        self.db.commit()

        image.id = cursor.lastrowid

        return image

    def get_all(self) -> list[Image]:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, title, url
            FROM images
            """
        )

        rows = cursor.fetchall()

        return [
            Image(
                id=row[0],
                title=row[1],
                url=row[2]
            )
            for row in rows
        ]

    def get_by_id(self, image_id: int) -> Image | None:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, title, url
            FROM images
            WHERE id = ?
            """,
            (image_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Image(
            id=row[0],
            title=row[1],
            url=row[2]
        )

    def update(self, image: Image) -> bool:
        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE images
            SET title = ?
            WHERE id = ?
            """,
            (image.title, image.id)
        )

        self.db.commit()

        return cursor.rowcount > 0

    def delete(self, image_id: int) -> bool:
        cursor = self.db.cursor()

        cursor.execute(
            """
            DELETE FROM images
            WHERE id = ?
            """,
            (image_id,)
        )

        self.db.commit()

        return cursor.rowcount > 0