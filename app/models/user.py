from app.enum.user_role import UserRole

class User:
    def __init__(
        self,
        id: int = None,
        firstname: str = None,
        role: UserRole = UserRole.NONE,
        password: str = None
    ):
        self.id = id
        self.firstname = firstname
        self.role = role
        self.password = password



        