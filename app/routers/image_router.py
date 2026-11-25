from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from uuid import uuid4
import shutil
from app.models.image import Image
from app.repositories.image_repository import ImageRepository
from app.db.connection import get_connection
from fastapi import Depends
from app.dependencies.authorisation import  require_role
from app.enum.user_role import UserRole


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)

IMAGES_DIR = Path(__file__).resolve().parent.parent / "static" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", dependencies=[Depends(require_role(UserRole.ADMIN))])
def create_image(
    title: str = Form(...),
    file: UploadFile = File(...)
):
    db = get_connection()
    repository = ImageRepository(db)

    # Vérifier le type de fichier
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Format d'image non autorisé"
        )

    # Générer un nom de fichier unique
    filename = f"{uuid4().hex}{extension}"
    file_path = IMAGES_DIR / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Générer automatiquement l'URL
        image_url = f"/static/images/{filename}"

        image = Image(
            title=title,
            url=image_url
        )

        created_image = repository.create(image)

        return {
            "id": created_image.id,
            "title": created_image.title,
            "url": created_image.url
        }

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

    finally:
        file.file.close()


@router.get("/")
def get_all_images():
    db = get_connection()
    repository = ImageRepository(db)

    images = repository.get_all()

    return [
        {
            "id": image.id,
            "title": image.title,
            "url": image.url
        }
        for image in images
    ]


@router.get("/{image_id}")
def get_image(image_id: int):
    db = get_connection()
    repository = ImageRepository(db)

    image = repository.get_by_id(image_id)

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image introuvable"
        )

    return {
        "id": image.id,
        "title": image.title,
        "url": image.url
    }


@router.put("/{image_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def update_image(
    image_id: int,
    title: str = Form(...)
):
    db = get_connection()
    repository = ImageRepository(db)

    image = repository.get_by_id(image_id)

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image introuvable"
        )

    image.title = title

    repository.update(image)

    return {
        "id": image.id,
        "title": image.title,
        "url": image.url
    }


@router.delete("/{image_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def delete_image(image_id: int):
    db = get_connection()
    repository = ImageRepository(db)

    image = repository.get_by_id(image_id)

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image introuvable"
        )

    filename = Path(image.url).name
    file_path = IMAGES_DIR / filename

    repository.delete(image_id)

    file_path.unlink(missing_ok=True)

    return {
        "message": "Image supprimée avec succès"
    }
