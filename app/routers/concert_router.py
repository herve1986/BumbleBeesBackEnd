from datetime import date, time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.concert import Concert
from app.repositories.concert_repository import ConcertRepository
from app.db.connection import get_connection
from fastapi import Depends
from app.dependencies.authorisation import  require_role
from app.enum.user_role import UserRole

router = APIRouter(
    prefix="/concerts",
    tags=["Concerts"],
)

class ConcertRequest(BaseModel):
    address: str | None = None
    city: str
    date_concert: date | None = None
    time_concert: time | None = None



@router.post("/", dependencies=[Depends(require_role(UserRole.ADMIN))])
def create_concert(concert_data: ConcertRequest):
    db = get_connection()
    repository = ConcertRepository(db)

    concert = Concert(
        address=concert_data.address,
        city=concert_data.city,
        date_concert=concert_data.date_concert,
        time_concert=concert_data.time_concert
    )

    created_concert = repository.create(concert)

    return {
        "id": created_concert.id,
        "address": created_concert.address,
        "city": created_concert.city,
        "date_concert": created_concert.date_concert,
        "time_concert": created_concert.time_concert
    }


@router.get("/")
def get_concerts():
    db = get_connection()
    repository = ConcertRepository(db)

    concerts = repository.get_all()

    return [
        {
            "id": concert.id,
            "address": concert.address,
            "city": concert.city,
            "date_concert": concert.date_concert,
            "time_concert": concert.time_concert
        }
        for concert in concerts
    ]


@router.get("/{concert_id}")
def get_concert(concert_id: int):
    db = get_connection()
    repository = ConcertRepository(db)

    concert = repository.get_by_id(concert_id)

    if concert is None:
        raise HTTPException(
            status_code=404,
            detail="Concert not found"
        )

    return {
        "id": concert.id,
        "address": concert.address,
        "city": concert.city,
        "date_concert": concert.date_concert,
        "time_concert": concert.time_concert
    }


@router.put("/{concert_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def update_concert(concert_id: int, concert_data: ConcertRequest):
    db = get_connection()
    repository = ConcertRepository(db)

    concert = repository.get_by_id(concert_id)

    if concert is None:
        raise HTTPException(
            status_code=404,
            detail="Concert not found"
        )

    concert.address = concert_data.address
    concert.city = concert_data.city
    concert.date_concert = concert_data.date_concert
    concert.time_concert = concert_data.time_concert

    repository.update(concert)

    return {
        "id": concert.id,
        "address": concert.address,
        "city": concert.city,
        "date_concert": concert.date_concert,
        "time_concert": concert.time_concert
    }


@router.delete("/{concert_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def delete_concert(concert_id: int):
    db = get_connection()
    repository = ConcertRepository(db)

    deleted = repository.delete(concert_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Concert not found"
        )

    return {
        "message": "Concert deleted successfully"
    }
