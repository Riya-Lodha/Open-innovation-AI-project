from images.v1.handlers.images_hand import ImagesHandler
from images.v1.validators.image_data import validate_depth_of_frames
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends


router = APIRouter(
    prefix="/images",
)

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        await ImagesHandler().upload_csv(request_data=file)
        return {"message": "CSV uploaded and processed successfully"}
    except HTTPException as e:
        return {"error": str(e)}


@router.get("/frames", description="Fetches the image frames based on the filters")
async def get_frames(filters: dict = Depends(validate_depth_of_frames)):
    params = filters
    
    handler_response = await ImagesHandler().fetch_image_frames_details(request_data=params)
    return handler_response
