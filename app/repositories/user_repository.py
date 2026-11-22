from app.models.user import User


class UserRepository:

    def __init__(self, db):
        self.db = db

    def create(self, user: User) -> User:
        cursor = self.db.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO users (firstname, password)
                VALUES (?, ?)
                """,
                (user.firstname, user.password)
            )

            self.db.commit()
            user.id = cursor.lastrowid

            return user

        except Exception:
            self.db.rollback()
            raise

        finally:
            cursor.close()