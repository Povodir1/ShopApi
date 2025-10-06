from fastapi import APIRouter,HTTPException,status, Depends
from app.services.favorite import serv_get_favorite_items,serv_add_to_favorite,serv_delete_from_favorite
from app.schemas.favorite import FavouriteItemSchema
from app.schemas.user import UserTokenDataSchema
from app.services.security import get_token
router = APIRouter(prefix="/favorite",tags = ["Favorite"])

@router.get("",response_model=list[FavouriteItemSchema])
def get_favorite(user:UserTokenDataSchema = Depends(get_token)):
    response = serv_get_favorite_items(user.id)
    return response

@router.post("/{item_id}",response_model=FavouriteItemSchema,status_code=status.HTTP_201_CREATED)
def add_to_favorite(item_id:int,user:UserTokenDataSchema = Depends(get_token)):
    try:
        response = serv_add_to_favorite(user.id,item_id)
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

@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_from_favorite(item_id,user:UserTokenDataSchema = Depends(get_token)):
    try:
        serv_delete_from_favorite(item_id,user.id)
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

