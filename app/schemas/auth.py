from pydantic import BaseModel


class LoginRequest(BaseModel):
    firstname: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
