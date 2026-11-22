
from app.core.security import hash_password
from app.models.user import User

class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, firstname: str, password: str):
        hashed_password = hash_password(password)

        user = User(
            firstname=firstname,
            password=hashed_password
        )

        return self.user_repository.create(user)


    