from fastapi import FastAPI
from contextlib import asynccontextmanager
from images.v1.api_router import image_v1_router
from database.sqllite_connection import SQLiteConnection


@asynccontextmanager
async def lifespan(_):
    """
    Function to create database connection and tables when server gets up.
    """
    db_connection = SQLiteConnection()
    await db_connection.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    docs_url="/images/documentation",
    redoc_url="/images/redoc",
)

app.include_router(image_v1_router, prefix="/innovation")
