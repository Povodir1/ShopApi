from fastapi import APIRouter, Depends

from app.models.role import RoleEnum
from app.services.api_crud.permission import db_get_all_permissions,db_add_permission,db_delete_permission,db_update_user_role
from app.services.security import check_permissions,get_token
from app.models.permission import ResourceEnum as Res, ActionEnum as Act
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.schemas.user import UserTokenDataSchema


router = APIRouter(prefix="/admin",tags=["Admin"])

@router.get("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.READ))])
def get_permissions(session:Session = Depends(get_session)):
    response = db_get_all_permissions(session)
    return response

@router.post("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.CREATE))])
def add_permissions(role:RoleEnum,
                    resource:Res,
                    action:Act,
                    user:UserTokenDataSchema = Depends(get_token),
                    session:Session = Depends(get_session)):
    response = db_add_permission(role,resource,action,user,session)
    return response

@router.delete("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.DELETE))])
def delete_permissions(role:RoleEnum,
                       resource:Res,
                       action:Act,
                       session:Session = Depends(get_session)):
    response = db_delete_permission(role,resource,action,session)
    return response

@router.patch("/role",dependencies=[Depends(check_permissions(Res.ROLES, Act.UPDATE))])
def update_role(role:RoleEnum,
                user:UserTokenDataSchema = Depends(get_token),
                session:Session = Depends(get_session)
                ):
    response = db_update_user_role(user.id,role, session)
    return response
