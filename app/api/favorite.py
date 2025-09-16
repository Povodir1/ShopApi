from fastapi import APIRouter,HTTPException,status
from app.services.favorite import serv_get_favorite_items,serv_add_to_favorite,serv_delete_from_favorite
router = APIRouter(prefix="/favorite",tags = ["Favorite"])

@router.get("")
def get_favorite(user_id:int):
    response = serv_get_favorite_items(user_id)
    return response

@router.post("/{item_id}")
def add_to_favorite(item_id:int,user_id:int):
    response = serv_add_to_favorite(user_id,item_id)
    return response

@router.delete("/{item_id}")
def delete_from_favorite(item_id,user_id):
    response = serv_delete_from_favorite(item_id,user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return {"msg": "Item deleted"}

