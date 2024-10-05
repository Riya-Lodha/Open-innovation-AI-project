from fastapi import APIRouter
from images.v1.controllers import images_cont

image_v1_router = APIRouter()

image_v1_router.include_router(
    images_cont.router, prefix="/api/v1"
)