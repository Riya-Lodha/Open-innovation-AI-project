from fastapi import Query, HTTPException


async def validate_depth_of_frames(
    depth_min: float = Query(alias="depthMin"),
    depth_max: float = Query(alias="depthMax"),
):

    if depth_min > depth_max:
        raise HTTPException(
            status_code=400,
            detail="Value of depth_min cannot be greater than value of depth_max",
        )

    return {"depthMin": depth_min, "depthMax": depth_max}
