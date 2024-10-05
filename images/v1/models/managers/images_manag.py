from sqlalchemy import select
from typing import List, Tuple
from sqlalchemy.orm import selectinload
from images.v1.models.models import Image
from database.sqllite_connection import SQLiteConnection

db_connection = SQLiteConnection()


class ImagesManager:

    async def insert_image_data(self, depth: float, pixels: bytes):
        async with db_connection.get_session() as session:
            async with session.begin():
                    if depth:
                        image_data = Image(depth=depth, pixels=pixels)
                        await session.merge(image_data)

    async def get_image_frames(self, depth_min: float, depth_max: float) -> List[Tuple[float, bytes]]:
        async with db_connection.get_session() as session:
            query = select(Image).filter(Image.depth.between(depth_min, depth_max)).options(selectinload('*'))
            result = await session.execute(query)
            images = result.scalars().all()
            return [(image.depth, image.pixels) for image in images]
