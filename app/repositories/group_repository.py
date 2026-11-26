from app.models.group import Group


class GroupRepository:

    def __init__(self, db):
        self.db = db

    def create(self, group: Group):
        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO groups (name)
            VALUES (?)
            """,
            (group.name,)
        )

        self.db.commit()

        group.id = cursor.lastrowid
        return group

    def get_all(self):
        cursor = self.db.cursor()

        cursor.execute("SELECT id, name FROM groups")

        rows = cursor.fetchall()

        return [
            Group(
                id=row[0],
                name=row[1]
            )
            for row in rows
        ]

    def get_by_id(self, group_id: int):
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT id, name FROM groups WHERE id = ?",
            (group_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Group(
            id=row[0],
            name=row[1]
        )

    def update(self, group: Group):
        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE groups
            SET name = ?
            WHERE id = ?
            """,
            (group.name, group.id)
        )

        self.db.commit()

        return cursor.rowcount > 0

    def delete(self, group_id: int):
        cursor = self.db.cursor()

        try:
            cursor.execute(
                "DELETE FROM musics WHERE group_id = ?",
                (group_id,)
            )

            cursor.execute(
                "DELETE FROM groups WHERE id = ?",
                (group_id,)
            )

            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        return cursor.rowcount > 0