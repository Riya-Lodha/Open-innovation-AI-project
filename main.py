from fastapi import FastAPI
from images.v1.api_router import image_v1_router
from database.sqllite_connection import SQLiteConnection
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_):
    db_connection = SQLiteConnection()
    await db_connection.init_db()
    yield

app = FastAPI(
    lifespan=lifespan,
    docs_url="/images/documentation",
    redoc_url="/images/redoc",
)

app.include_router(image_v1_router, prefix="/innovation")
