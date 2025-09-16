from fastapi import APIRouter
from fastapi import HTTPException,status
from app.services.basket import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket

router = APIRouter(prefix="/basket",tags=["Basket"])


@router.get("")
def get_basket(user_id:int):
    response = serv_get_basket_items(user_id)
    return response

@router.post("/{item_id}")
def add_to_basket(item_id:int,user_id:int):
    response = serv_add_to_basket(user_id,item_id)
    return response

@router.delete("/{item_id}")
def delete_from_basket(item_id,user_id):
    response = serv_delete_from_basket(item_id,user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return {"msg": "Item deleted"}


