import cv2
import io
import math
import numpy as np
import pandas as pd
from fastapi import UploadFile, HTTPException
from images.v1.models.managers.images_manager import ImagesManager


class ImagesHandler:
    def __init__(self) -> None:
        self.image_manager = ImagesManager()
        self.batch_size = 100

    async def upload_csv(self, request_data: UploadFile):
        """
        Handler method to upload csv file containing image frames.
        Args:
            request_data (dict): File containing images to be uploaded in batch wise in sqllite database.
        """

        contents = await request_data.read()
        data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        column_names = data.columns.tolist()
        if "depth" not in column_names:
            raise HTTPException(
                status_code=400, detail="'depth' column is mandatory in file"
            )
        data = data.set_index("depth")
        batch = []

        for depth, row in data.iterrows():
            if depth and not math.isnan(depth):
                resized_row = (
                    cv2.resize(np.array(row).reshape(1, -1), (150, 1))
                    .flatten()
                    .astype(np.float32)
                )
                batch.append((depth, resized_row.tobytes()))

                if len(batch) >= self.batch_size:
                    await self.image_manager.insert_image_data_batch(batch)
                    batch.clear()

        if batch:
            await self.image_manager.insert_image_data_batch(batch)

    async def fetch_image_frames_details(self, request_data: dict):
        """
        Handler method to retrieve a list of image frames based on the depth.
        Args:
            request_data (dict): Dictionary that includes minimum depth and maximum depth.
        Returns:
            Dict: A dict of image frames
        """

        depth_min = request_data.get("depthMin")
        depth_max = request_data.get("depthMax")

        rows = await self.image_manager.get_image_frames(depth_min, depth_max)

        frames = []
        for depth, pixels in rows:
            pixel_array = np.frombuffer(pixels, dtype=np.float32)
            pixel_array = pixel_array.reshape((1, 150))

            normalized_pixel_array = cv2.normalize(
                pixel_array, None, 0, 255, cv2.NORM_MINMAX
            )
            normalized_pixel_array = normalized_pixel_array.astype(np.uint8)

            colored_frame = cv2.applyColorMap(normalized_pixel_array, cv2.COLORMAP_JET)

            pixel_tuples = [
                tuple(int(c) for c in colored_frame[0, i])
                for i in range(colored_frame.shape[1])
            ]

            frames.append({"depth": depth, "pixel": pixel_tuples})
        return {"data": frames}
