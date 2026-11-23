from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.music import Music
from app.repositories.music_repository import MusicRepository
from app.repositories.group_repository import GroupRepository
from app.db.connection import get_connection


router = APIRouter(
    prefix="/musics",
    tags=["Musics"]
)


class MusicRequest(BaseModel):
    title: str
    group_id: int


@router.post("/")
def create_music(music_data: MusicRequest):
    db = get_connection()

    music_repository = MusicRepository(db)
    group_repository = GroupRepository(db)

    # Vérifier que le groupe existe
    group = group_repository.get_by_id(music_data.group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    music = Music(
        title=music_data.title,
        group_id=music_data.group_id
    )

    created_music = music_repository.create(music)

    return {
        "id": created_music.id,
        "title": created_music.title,
        "group_id": created_music.group_id
    }


@router.get("/")
def get_musics():
    db = get_connection()
    repository = MusicRepository(db)

    musics = repository.get_all()

    return [
        {
            "id": music.id,
            "title": music.title,
            "group_id": music.group_id
        }
        for music in musics
    ]


@router.get("/group/{group_id}")
def get_musics_by_group(group_id: int):
    db = get_connection()

    group_repository = GroupRepository(db)
    music_repository = MusicRepository(db)

    group = group_repository.get_by_id(group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    musics = music_repository.get_by_group_id(group_id)

    return [
        {
            "id": music.id,
            "title": music.title,
            "group_id": music.group_id
        }
        for music in musics
    ]


@router.get("/{music_id}")
def get_music(music_id: int):
    db = get_connection()
    repository = MusicRepository(db)

    music = repository.get_by_id(music_id)

    if music is None:
        raise HTTPException(
            status_code=404,
            detail="Music not found"
        )

    return {
        "id": music.id,
        "title": music.title,
        "group_id": music.group_id
    }


@router.put("/{music_id}")
def update_music(music_id: int, music_data: MusicRequest):
    db = get_connection()

    music_repository = MusicRepository(db)
    group_repository = GroupRepository(db)

    music = music_repository.get_by_id(music_id)

    if music is None:
        raise HTTPException(
            status_code=404,
            detail="Music not found"
        )

    group = group_repository.get_by_id(music_data.group_id)

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )

    music.title = music_data.title
    music.group_id = music_data.group_id

    music_repository.update(music)

    return {
        "id": music.id,
        "title": music.title,
        "group_id": music.group_id
    }


@router.delete("/{music_id}")
def delete_music(music_id: int):
    db = get_connection()
    repository = MusicRepository(db)

    deleted = repository.delete(music_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Music not found"
        )

    return {
        "message": "Music deleted successfully"
    }