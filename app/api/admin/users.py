from fastapi import APIRouter, HTTPException, status, Depends

from app.services.api_crud.user import change_role,ban_user
from app.models.user import Role
from app.services.security import is_admin

router = APIRouter(prefix="/users",tags=["Users"],dependencies=[Depends(is_admin)])

@router.patch("/change_role")
def change_user_role(user_id:int,role:Role):
    try:
        response = change_role(user_id,role)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/ban")
def ban_user(user_id:int,is_banned:bool = True):
    try:
        response = ban_user(user_id,is_banned)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
