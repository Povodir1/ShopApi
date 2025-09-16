from fastapi import APIRouter
from app.services.comments import serv_get_comments
router = APIRouter(prefix="/comments",tags=["Comments"])

#юзер по токену

@router.get("/{item_id}")
def get_comments(item_id:int):
    return serv_get_comments(item_id)

@router.patch("/{item_id}")
def patch_comments(item_id:int, user:str):
    pass

@router.delete("/{item_id}")
def delete_comments(item_id:int, user:str):
    pass

@router.post("/{item_id}")
def post_comments(item_id:int, user:str):
    pass







