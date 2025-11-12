from fastapi import APIRouter,status, Depends

from app.api.favorite.services import serv_get_favorite_items,serv_add_to_favorite,serv_delete_from_favorite
from app.api.favorite.schemas import FavouriteItemSchema

from app.core.dependencies import TokenDep,check_permissions,SessionDep

from app.core.enums import ResourceEnum as Res, ActionEnum as Act



router = APIRouter(prefix="/favorite",tags = ["Favorite"])

@router.get("",response_model=list[FavouriteItemSchema],
            dependencies=[Depends(check_permissions(Res.FAVORITE_ITEMS, Act.READ))])
def get_favorite(user:TokenDep,
                 session:SessionDep):
    response = serv_get_favorite_items(user.id,session)
    return response

@router.post("/{item_id}",response_model=FavouriteItemSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.FAVORITE_ITEMS, Act.CREATE))])
def add_to_favorite(item_id:int,
                    user:TokenDep,
                    session: SessionDep
                    ):
    response = serv_add_to_favorite(user.id,item_id,session)
    return response

@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(check_permissions(Res.FAVORITE_ITEMS, Act.DELETE))])
def delete_from_favorite(item_id:int,
                         user:TokenDep,
                         session: SessionDep
                         ):
    serv_delete_from_favorite(item_id,user.id,session)
    return {"msg": "Item deleted"}

