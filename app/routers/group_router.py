from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.group import Group
from app.repositories.group_repository import GroupRepository
from app.db.connection import get_connection


router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


class GroupRequest(BaseModel):
    name: str


@router.post("/")
def create_group(group_data: GroupRequest):
    db = get_connection()
    repository = GroupRepository(db)

    group = Group(name=group_data.name)

    created_group = repository.create(group)

    return {
        "id": created_group.id,
        "name": created_group.name
    }


@router.get("/")
def get_groups():
    db = get_connection()
    repository = GroupRepository(db)

    groups = repository.get_all()

    return [
        {
            "id": group.id,
            "name": group.name
        }
        for group in groups
    ]


@router.get("/{group_id}")
def get_group(group_id: int):
    db = get_connection()
    repository = GroupRepository(db)

    group = repository.get_by_id(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return {
        "id": group.id,
        "name": group.name
    }


@router.put("/{group_id}")
def update_group(group_id: int, group_data: GroupRequest):
    db = get_connection()
    repository = GroupRepository(db)

    group = repository.get_by_id(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    group.name = group_data.name

    repository.update(group)

    return {
        "id": group.id,
        "name": group.name
    }


@router.delete("/{group_id}")
def delete_group(group_id: int):
    db = get_connection()
    repository = GroupRepository(db)

    deleted = repository.delete(group_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    return {
        "message": "Group deleted successfully"
    }