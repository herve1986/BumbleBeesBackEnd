import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)



def create_access_token(user_id: int) -> str:

    if not SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is missing")

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )



def verify_access_token(token: str) -> int | None:

    if not SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is missing")

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None

