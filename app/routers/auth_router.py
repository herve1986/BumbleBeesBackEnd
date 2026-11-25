from fastapi import APIRouter, Depends, HTTPException, status
from app.db.connection import get_connection
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.auth import LoginRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_auth_service(db=Depends(get_connection)):
    repository = UserRepository(db)
    return UserService(repository)


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    service: UserService = Depends(get_auth_service)
):
    token = service.login(
        credentials.firstname,
        credentials.password
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect firstname or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
