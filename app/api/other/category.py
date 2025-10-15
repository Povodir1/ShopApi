
from fastapi import APIRouter,Depends

from app.services.api_crud.item import  serv_get_categories
from app.database import get_session
from sqlalchemy.orm.session import Session


router = APIRouter(tags=["Category"])

@router.get("/category")
def get_categories(session:Session = Depends(get_session)):
    response = serv_get_categories(session)
    return response
