from fastapi import APIRouter, Depends

from app.services.api_crud.user import change_role,ban_user
from app.services.security import check_permissions
from app.models.permission import ResourceEnum as Res, ActionEnum as Act
from app.database import get_session
from sqlalchemy.orm.session import Session
router = APIRouter(prefix="/users",tags=["Users"])

@router.patch("/change_role",dependencies=[Depends(check_permissions(Res.ROLES, Act.UPDATE))])
def change_user_role(user_id:int,
                     role:str,
                     session:Session = Depends(get_session)):
    response = change_role(user_id,role,session)
    return response


@router.patch("/ban",dependencies=[Depends(check_permissions(Res.USERS, Act.DELETE))])
def ban_user(user_id:int,
             is_banned:bool = True,
             session:Session = Depends(get_session)):
    response = ban_user(user_id,is_banned,session)
    return response

