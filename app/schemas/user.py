from pydantic import BaseModel
from app.enum.user_role import UserRole


class UserCreate(BaseModel):
    firstname: str
    role : UserRole
    password: str


class UserResponse(BaseModel):
    id: int
    firstname: str
    role: UserRole