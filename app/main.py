
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import user_router, group_router, music_router, concert_router, image_router
from app.db.init_db import init_db
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware




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


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(group_router.router)
app.include_router(music_router.router)
app.include_router(concert_router.router)
app.include_router(image_router.router)


IMAGES_DIR = Path(__file__).resolve().parent / "static" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/static/images",
    StaticFiles(directory=IMAGES_DIR),
    name="images"
)

