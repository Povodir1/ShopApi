from fastapi import APIRouter,HTTPException,status
from app.services.favorite import serv_get_favorite_items,serv_add_to_favorite,serv_delete_from_favorite
router = APIRouter(prefix="/favorite",tags = ["Favorite"])

@router.get("")
def get_favorite(user_id:int):
    response = serv_get_favorite_items(user_id)
    return response

@router.post("/{item_id}")
def add_to_favorite(item_id:int,user_id:int):
    try:
        response = serv_add_to_favorite(user_id,item_id)
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

@router.delete("/{item_id}")
def delete_from_favorite(item_id,user_id):
    try:
        serv_delete_from_favorite(item_id,user_id)
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

