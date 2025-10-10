

from fastapi import APIRouter,HTTPException,status

from fastapi.params import Depends

from app.services.api_crud.item import serv_get_item, get_all_items, serv_get_categories,SortType
from app.schemas.item import ItemFilterSchema,get_filters,ItemCatalogSchema,ItemSoloSchema
from app.schemas.user import UserTokenDataSchema
from app.services.security import get_token

from app.models.user import CurrencyType

router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all",response_model=list[ItemCatalogSchema])
def get_item_all(filters:ItemFilterSchema = Depends(get_filters),
                 limit:int = 10,
                 page:int = 1,
                 sort_type:SortType = SortType.by_rating,
                 user:UserTokenDataSchema = Depends(get_token)):
    try:
        response = get_all_items(limit,page,sort_type,filters,user.id,CurrencyType[user.currency])
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )



@router.get("/category")
def get_categories():
    response = serv_get_categories()
    return response


@router.get("/{item_id}",response_model=ItemSoloSchema)
def get_item(item_id,user:UserTokenDataSchema = Depends(get_token)):
    try:
        response = serv_get_item(item_id,user.id if user else None)
        return response
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




