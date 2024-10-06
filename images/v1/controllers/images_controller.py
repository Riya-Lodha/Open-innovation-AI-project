from images.v1.handlers.images_handler import ImagesHandler
from images.v1.validators.image_data import validate_depth_of_frames
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends


router = APIRouter(
    prefix="/images",
)


@router.post("/upload-csv", description="Upload the csv containing image frames")
async def upload_csv(file: UploadFile = File(...)):
    """
    Controller method to upload csv file containing image frames.
    Args:
        file: Uploaded File
    Returns:
        Acknowledge message stating the file has been uploaded successfully
        Raise HTTPException error if error in file.
    """

    try:
        await ImagesHandler().upload_csv(request_data=file)
        return {"message": "CSV uploaded and processed successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=str(e.detail))


@router.get("/frames", description="Fetches the image frames based on the filters")
async def get_frames(filters: dict = Depends(validate_depth_of_frames)):
    """
    Controller method to fetch image frames based on the depth
    Args:
        filters: Dictionary containing minimum depth and maximum depth
    Returns:
        Images with depth and pixel in coloured map
    """

    params = filters

    handler_response = await ImagesHandler().fetch_image_frames_details(
        request_data=params
    )
    return handler_response
