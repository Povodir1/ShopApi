from fastapi import APIRouter
from fastapi import HTTPException,status
from app.services.basket import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket

router = APIRouter(prefix="/basket",tags=["basket"])


@router.get("")
def get_basket(user_id:int):
    return serv_get_basket_items(user_id)

@router.post("/{item_id}")
def add_to_basket(item_id:int,user_id:int):
    return serv_add_to_basket(user_id,item_id)

@router.delete("/{item_id}")
def delete_from_basket(item_id,user_id):
    response = serv_delete_from_basket(item_id,user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return {"msg": "Item deleted"}


