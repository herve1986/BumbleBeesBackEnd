from fastapi import APIRouter, Depends
from typing import Iterator
from app.db.connection import get_connection
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


def get_user_service() -> Iterator[UserService]:
    db = get_connection()

    try:
        repository = UserRepository(db)
        yield UserService(repository)
    finally:
        db.close()


@router.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(
        user.firstname,
        user.password
    )