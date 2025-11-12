from fastapi import APIRouter,status,Depends
from app.api.basket.services import serv_add_to_basket, serv_get_basket_items,serv_delete_from_basket
from app.api.basket.schemas import BasketSchema, BasketItemSchema

from app.core.dependencies import TokenDep,check_permissions,SessionDep

from app.models.user import CurrencyType
from app.models.permission import ResourceEnum as Res, ActionEnum as Act


router = APIRouter(prefix="/basket",tags=["Basket"])


@router.get("",response_model=BasketSchema,
            dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.READ))])
def get_basket(user:TokenDep,
               session:SessionDep
               ):
    response = serv_get_basket_items(user.id,CurrencyType(user.currency),session)
    return response

@router.post("/{item_id}",response_model=BasketItemSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.CREATE))])
def add_to_basket(item_id:int,
                  count:int,
                  user:TokenDep,
                  session:SessionDep
                  ):
    response = serv_add_to_basket(user.id,item_id,count,CurrencyType(user.currency),session)
    return response


@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(check_permissions(Res.BASKET_ITEMS, Act.DELETE))])
def delete_from_basket(item_id:int,
                       user:TokenDep,
                       session:SessionDep
                       ):
    serv_delete_from_basket(item_id,user.id,session)
    return {"msg": "Item deleted"}


