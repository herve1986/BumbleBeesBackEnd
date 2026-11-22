from contextlib import asynccontextmanager
from app.routers import user_router
from fastapi import FastAPI, HTTPException
from app.db.connection import get_connection
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation de la base de données
    init_db()

    yield

    # Code exécuté à l'arrêt de l'application

app = FastAPI(
    title="BumbleBees API",
    description="Backend de BumbleBees",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_router.router)


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
        db.close()

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
