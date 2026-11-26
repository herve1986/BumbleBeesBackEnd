import uuid
import boto3

from app.core.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
    aws_access_key_id=settings.r2_access_key_id,
    aws_secret_access_key=settings.r2_secret_access_key,
    region_name="auto",
)

BUCKET = settings.r2_bucket
PUBLIC_URL = settings.r2_public_url.rstrip("/")


def upload_image(file, extension: str, content_type: str) -> str:
    """Envoie l'image dans R2 et renvoie son URL publique."""
    filename = f"{uuid.uuid4().hex}{extension}"

    s3.upload_fileobj(
        file,
        BUCKET,
        filename,
        ExtraArgs={"ContentType": content_type},
    )

    return f"{PUBLIC_URL}/{filename}"


def delete_image(url: str) -> None:
    """Supprime l'image de R2 à partir de son URL."""
    filename = url.rsplit("/", 1)[-1]
    s3.delete_object(Bucket=BUCKET, Key=filename)