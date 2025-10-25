

from fastapi import APIRouter

from fastapi.params import Depends

from app.services.api_crud.item import serv_get_item, get_all_items,SortType
from app.schemas.item import ItemFilterSchema,get_filters,CatalogSchema,ItemSoloSchema
from app.schemas.user import UserTokenDataSchema
from app.services.security import get_token
from app.database import get_session
from sqlalchemy.orm.session import Session

from app.models.user import CurrencyType

router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all",response_model=CatalogSchema)
def get_item_all(filters:ItemFilterSchema = Depends(get_filters),
                 limit:int = 10,
                 page:int = 1,
                 sort_type:SortType = SortType.by_rating,
                 user:UserTokenDataSchema = Depends(get_token),
                 session:Session = Depends(get_session)
                 ):
    response = get_all_items(limit,page,sort_type,filters,user.id,CurrencyType[user.currency],session)
    return response



@router.get("/{item_id}",response_model=ItemSoloSchema)
def get_item(item_id:int,
             user:UserTokenDataSchema = Depends(get_token),
             session:Session = Depends(get_session)
             ):
    response = serv_get_item(item_id,user.id if user else None,CurrencyType(user.currency),session)
    return response





