from fastapi import APIRouter, HTTPException, status, Depends

from app.services.api_crud.user import change_role,ban_user
from app.models.user import Role
from app.services.security import is_admin
from app.database import get_session
from sqlalchemy.orm.session import Session
router = APIRouter(prefix="/users",tags=["Users"],dependencies=[Depends(is_admin)])

@router.patch("/change_role")
def change_user_role(user_id:int,role:Role,session:Session = Depends(get_session)):
    try:
        response = change_role(user_id,role,session)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.patch("/ban")
def ban_user(user_id:int,is_banned:bool = True,session:Session = Depends(get_session)):
    try:
        response = ban_user(user_id,is_banned,session)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
