from fastapi import APIRouter
from fastapi import HTTPException,status,Depends
from app.services.api_crud.basket import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket
from app.schemas.basket_item import BasketSchema, BasketItemSchema
from app.schemas.user import UserTokenDataSchema
from app.services.security import get_token
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.models.user import CurrencyType
from app.services.security import check_permissions
from app.models.permission import ResourceEnum as Res, ActionEnum as Act
router = APIRouter(prefix="/basket",tags=["Basket"])


@router.get("",response_model=BasketSchema,
            dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.READ))])
def get_basket(user:UserTokenDataSchema = Depends(get_token),
               session:Session = Depends(get_session)
               ):
    response = serv_get_basket_items(user.id,CurrencyType(user.currency),session)
    return response

@router.post("/{item_id}",response_model=BasketItemSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.CREATE))])
def add_to_basket(item_id:int,
                  count:int,
                  user:UserTokenDataSchema = Depends(get_token),
                  session:Session = Depends(get_session)
                  ):
    response = serv_add_to_basket(user.id,item_id,count,CurrencyType(user.currency),session)
    return response


@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.DELETE))])
def delete_from_basket(item_id:int,
                       user:UserTokenDataSchema = Depends(get_token),
                       session:Session = Depends(get_session)
                       ):
    serv_delete_from_basket(item_id,user.id,session)
    return {"msg": "Item deleted"}


