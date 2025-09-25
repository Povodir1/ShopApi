from fastapi import APIRouter
from fastapi import HTTPException,status,Depends
from app.services.basket import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket
from app.services.user import user_by_token
from app.schemas.basket_item import BasketItemSchema
from app.schemas.user import UserToken
router = APIRouter(prefix="/basket",tags=["Basket"])


@router.get("",response_model=list[BasketItemSchema])
def get_basket(user_id:int):
    response = serv_get_basket_items(user_id)
    return response

@router.post("/{item_id}",response_model=BasketItemSchema,status_code=status.HTTP_201_CREATED)
def add_to_basket(item_id:int,user_id:int):
    try:
        response = serv_add_to_basket(user_id,item_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_from_basket(item_id,user_id:int):
    try:
        serv_delete_from_basket(item_id,user_id)
        return {"msg": "Item deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


