
import libsql

from app.core.config import settings


def get_connection():
    return libsql.connect(
        settings.TURSO_DATABASE_URL,
        auth_token=settings.TURSO_AUTH_TOKEN
    )
