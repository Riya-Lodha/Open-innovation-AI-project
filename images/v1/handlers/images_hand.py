import cv2
import io
import math
import numpy as np
import pandas as pd
from fastapi import UploadFile
from images.v1.models.managers.images_manag import ImagesManager


class ImagesHandler:
    def __init__(self) -> None:
        self.image_manager = ImagesManager()

    async def fetch_image_frames_details(self, request_data: dict):
        depth_min = request_data.get("depthMin")
        depth_max = request_data.get("depthMax")

        rows = await self.image_manager.get_image_frames(depth_min, depth_max)

        frames = []
        for depth, pixels in rows:
            pixel_array = np.frombuffer(pixels, dtype=np.float32)
            pixel_array = pixel_array.reshape((1, 150))
            
            normalized_pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX)
            normalized_pixel_array = normalized_pixel_array.astype(np.uint8)

            colored_frame = cv2.applyColorMap(normalized_pixel_array, cv2.COLORMAP_JET)
            
            pixel_tuples = [tuple(int(c) for c in colored_frame[0, i]) for i in range(colored_frame.shape[1])]

            frames.append({
                "depth": depth,
                "pixel": pixel_tuples
            })
        return {"data": frames}
    
    async def upload_csv(self, request_data: UploadFile):
        contents = await request_data.read()
        data = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        data = data.set_index('depth')

        for depth, row in data.iterrows():
            if depth and not math.isnan(depth):
                resized_row = cv2.resize(np.array(row).reshape(1, -1), (150, 1)).flatten().astype(np.float32)

                await self.image_manager.insert_image_data(depth, resized_row.tobytes())
        