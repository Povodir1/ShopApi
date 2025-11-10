from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix="/image",tags=["Image"])


@router.get("/")
def get_image(image_url:str):
    return FileResponse(image_url)
