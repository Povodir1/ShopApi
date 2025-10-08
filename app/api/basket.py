from fastapi import APIRouter
from fastapi import HTTPException,status,Depends
from app.services.api_crud.basket import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket
from app.schemas.basket_item import BasketItemSchema
from app.schemas.user import UserTokenDataSchema
from app.services.security import get_token
router = APIRouter(prefix="/basket",tags=["Basket"])


@router.get("",response_model=list[BasketItemSchema])
def get_basket(user:UserTokenDataSchema = Depends(get_token)):
    if not user:
        return []
    response = serv_get_basket_items(user.id)
    return response

@router.post("/{item_id}",response_model=BasketItemSchema,status_code=status.HTTP_201_CREATED)
def add_to_basket(item_id:int,user:UserTokenDataSchema = Depends(get_token)):
    try:
        response = serv_add_to_basket(user.id,item_id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_from_basket(item_id,user:UserTokenDataSchema = Depends(get_token)):
    try:
        serv_delete_from_basket(item_id,user.id)
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


