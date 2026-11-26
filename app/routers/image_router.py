from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
from app.models.image import Image
from app.repositories.image_repository import ImageRepository
from app.db.connection import get_connection
from fastapi import Depends
from app.dependencies.authorisation import require_role
from app.enum.user_role import UserRole
from app.services.r2 import upload_image, delete_image


router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


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

    try:
        # 1. Envoi dans R2, on récupère l'URL
        image_url = upload_image(
            file.file,
            extension,
            file.content_type or "application/octet-stream"
        )

        # 2. Enregistrement de l'URL dans Turso
        image = Image(title=title, url=image_url)
        created_image = repository.create(image)

        return {
            "id": created_image.id,
            "title": created_image.title,
            "url": created_image.url
        }

    except Exception:
        # Si la base échoue, on retire l'image de R2 pour ne pas laisser un fichier orphelin
        if "image_url" in locals():
            delete_image(image_url)
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
def delete_image_route(image_id: int):
    db = get_connection()
    repository = ImageRepository(db)

    image = repository.get_by_id(image_id)

    if image is None:
        raise HTTPException(
            status_code=404,
            detail="Image introuvable"
        )

    repository.delete(image_id)
    delete_image(image.url)  # supprime aussi le fichier dans R2

    return {
        "message": "Image supprimée avec succès"
    }
