
from datetime import date, time

from app.models.concert import Concert


class ConcertRepository:

    def __init__(self, db):
        self.db = db

    def create(self, concert: Concert) -> Concert:
        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO concerts (address, city, date, hour)
            VALUES (?, ?, ?, ?)
            """,
            (
                concert.address,
                concert.city,
                concert.date_concert.isoformat() if concert.date_concert else None,
                concert.time_concert.isoformat() if concert.time_concert else None
            )
        )

        self.db.commit()
        concert.id = cursor.lastrowid

        return concert

    def get_all(self) -> list[Concert]:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, address, city, date, hour
            FROM concerts
            """
        )

        rows = cursor.fetchall()

        return [
            Concert(
                id=row[0],
                address=row[1],
                city=row[2],
                date_concert=date.fromisoformat(row[3]) if row[3] else None,
                time_concert=time.fromisoformat(row[4]) if row[4] else None
            )
            for row in rows
        ]

    def get_by_id(self, concert_id: int) -> Concert | None:
        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT id, address, city, date, hour
            FROM concerts
            WHERE id = ?
            """,
            (concert_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Concert(
            id=row[0],
            address=row[1],
            city=row[2],
            date_concert=date.fromisoformat(row[3]) if row[3] else None,
            time_concert=time.fromisoformat(row[4]) if row[4] else None
        )

    def update(self, concert: Concert) -> None:
        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE concerts
            SET address = ?, city = ?, date = ?, hour = ?
            WHERE id = ?
            """,
            (
                concert.address,
                concert.city,
                concert.date_concert.isoformat() if concert.date_concert else None,
                concert.time_concert.isoformat() if concert.time_concert else None,
                concert.id
            )
        )

        self.db.commit()

    def delete(self, concert_id: int) -> bool:
        cursor = self.db.cursor()

        cursor.execute(
            """
            DELETE FROM concerts
            WHERE id = ?
            """,
            (concert_id,)
        )

        self.db.commit()

        return cursor.rowcount > 0
