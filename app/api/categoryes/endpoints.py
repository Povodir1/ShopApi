from fastapi import APIRouter

from app.api.categoryes.services import serv_get_categories

from app.core.dependencies import SessionDep


router = APIRouter(tags=["Category"])

@router.get("/category")
def get_categories(session:SessionDep):
    response = serv_get_categories(session)
    return response
