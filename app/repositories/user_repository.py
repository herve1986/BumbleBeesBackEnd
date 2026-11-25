from app.models.user import User
from app.enum.user_role import UserRole


class UserRepository:

    def __init__(self, db):
        self.db = db

    def create(self, user: User) -> User:
        cursor = self.db.cursor()

        try:
            
            cursor.execute(
                """
                INSERT INTO users (firstname, role, password)
                VALUES (?, ?, ?)
                """,
                (user.firstname, user.role.value, user.password)
            )

            self.db.commit()
            user.id = cursor.lastrowid

            return user

        except Exception:
            self.db.rollback()
            raise

        finally:
            cursor.close()


    def get_by_firstname(self, firstname: str) -> User | None:
        cursor = self.db.cursor()

        try:
            cursor.execute(
                "SELECT * FROM users WHERE firstname = ?",
                (firstname,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return User(
                id=row[0],
                firstname = row[1],
                role = UserRole(row[2]),
                password = row[3]
            )

        finally:
            cursor.close()


    def get_by_id(self, user_id: int) -> User | None:
        cursor = self.db.cursor()

        try:
            cursor.execute(
                "SELECT id, firstname, role, password FROM users WHERE id = ?",
                (user_id,)
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return User(
                id=row[0],
                firstname=row[1],
                role=UserRole(row[2]),
                password=row[3]
            )

        finally:
            cursor.close()