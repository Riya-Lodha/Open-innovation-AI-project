from sqlalchemy import select
from datetime import datetime
from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from images.v1.models.models import Image
from database.sqllite_connection import SQLiteConnection

db_connection = SQLiteConnection()


class ImagesManager:
    async def insert_image_data_batch(self, batch: list):
        """
        Function to insert image frames inside Images table in Innovation DB.
        """
        async with db_connection.get_session() as session:
            async with session.begin():
                image_data_list = []
                for depth, pixels in batch:
                    if depth:
                        try:
                            existing_image = await session.execute(
                                select(Image).where(Image.depth == depth)
                            )
                            existing_image = existing_image.scalars().first()
                            if existing_image:

                                existing_image.pixels = pixels
                                existing_image.uploaded_on = datetime.utcnow()
                                image_data_list.append(existing_image)
                            else:
                                image_data = Image(
                                    depth=depth,
                                    pixels=pixels,
                                    uploaded_on=datetime.utcnow(),
                                )
                                image_data_list.append(image_data)
                        except HTTPException as e:
                            print(f"Error creating image data for depth {depth}: {e}")

                if image_data_list:
                    session.add_all(image_data_list)

    async def get_image_frames(
        self, depth_min: float, depth_max: float
    ) -> List[Tuple[float, bytes]]:
        """
        Function to fetch frames from Images table based on depth.
        """

        async with db_connection.get_session() as session:
            query = (
                select(Image)
                .filter(Image.depth.between(depth_min, depth_max))
                .options(selectinload("*"))
            )
            result = await session.execute(query)
            images = result.scalars().all()
            return [(image.depth, image.pixels) for image in images]
