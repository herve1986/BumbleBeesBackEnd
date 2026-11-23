from app.models.music import Music


class MusicRepository:

    def __init__(self, db):
        self.db = db

    def create(self, music: Music) -> Music:
        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO musics (title, group_id)
            VALUES (?, ?)
            """,
            (music.title, music.group_id)
        )

        self.db.commit()

        music.id = cursor.lastrowid

        return music

    def get_all(self) -> list[Music]:
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT id, title, group_id FROM musics"
        )

        rows = cursor.fetchall()

        return [
            Music(
                id=row[0],
                title=row[1],
                group_id=row[2]
            )
            for row in rows
        ]

    def get_by_id(self, music_id: int) -> Music | None:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, title, group_id
            FROM musics
            WHERE id = ?
            """,
            (music_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Music(
            id=row[0],
            title=row[1],
            group_id=row[2]
        )

    def get_by_group_id(self, group_id: int) -> list[Music]:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, title, group_id
            FROM musics
            WHERE group_id = ?
            """,
            (group_id,)
        )

        rows = cursor.fetchall()

        return [
            Music(
                id=row[0],
                title=row[1],
                group_id=row[2]
            )
            for row in rows
        ]

    def update(self, music: Music) -> None:
        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE musics
            SET title = ?, group_id = ?
            WHERE id = ?
            """,
            (music.title, music.group_id, music.id)
        )

        self.db.commit()

    def delete(self, music_id: int) -> bool:
        cursor = self.db.cursor()

        cursor.execute(
            "DELETE FROM musics WHERE id = ?",
            (music_id,)
        )

        self.db.commit()

        return cursor.rowcount > 0