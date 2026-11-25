from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.models.user import User
from app.enum.user_role import UserRole



class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, firstname: str, role: str, password: str):
        hashed_password = hash_password(password)

        user = User(
            firstname = firstname,
            role = UserRole(role),
            password = hashed_password
        )

        return self.user_repository.create(user)

    def login(self, firstname: str, password: str) -> str | None:
        user = self.user_repository.get_by_firstname(firstname)

        if user is None:
            return None

        if not verify_password(password, user.password):
            return None

        return create_access_token(user.id)
