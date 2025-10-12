
from fastapi import APIRouter

from app.services.api_crud.item import  serv_get_categories


router = APIRouter(tags=["Category"])

@router.get("/category")
def get_categories():
    response = serv_get_categories()
    return response
