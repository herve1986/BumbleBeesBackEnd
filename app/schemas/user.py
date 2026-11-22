from pydantic import BaseModel


class UserCreate(BaseModel):
    firstname: str
    password: str


class UserResponse(BaseModel):
    id: int
    firstname: str