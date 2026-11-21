
from fastapi import FastAPI, HTTPException

from app.db.connection import get_connection

app = FastAPI(
    title="BumbleBees API",
    description="Backend de BumbleBees",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Bienvenue sur BumbleBees API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/health/database")
def database_health():
    try:
        db = get_connection()
        result = db.execute("SELECT 1").fetchone()

        return {
            "status": "ok",
            "database": "connected",
            "test": result[0]
        }

    except Exception as e:
        print(f"ERREUR TURSO : {type(e).__name__}: {e}")

        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )
