from fastapi import APIRouter, Depends

from app.api.permissions.services import db_get_all_permissions,db_add_permission,db_delete_permission,db_update_user_role

from app.core.dependencies import TokenDep,check_permissions,SessionDep
from app.core.enums import ResourceEnum as Res, ActionEnum as Act, RoleEnum




router = APIRouter(prefix="/admin",tags=["Permissions","Admin"])

@router.get("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.READ))])
def get_permissions(session: SessionDep):
    response = db_get_all_permissions(session)
    return response

@router.post("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.CREATE))])
def add_permissions(role:RoleEnum,
                    resource:Res,
                    action:Act,
                    user:TokenDep,
                    session: SessionDep):
    response = db_add_permission(role,resource,action,user,session)
    return response

@router.delete("/permissions",dependencies=[Depends(check_permissions(Res.PERMISSIONS, Act.DELETE))])
def delete_permissions(role:RoleEnum,
                       resource:Res,
                       action:Act,
                       session: SessionDep):
    response = db_delete_permission(role,resource,action,session)
    return response

@router.patch("/role",dependencies=[Depends(check_permissions(Res.ROLES, Act.UPDATE))])
def update_role(role:RoleEnum,
                user_id:int,
                session: SessionDep
                ):
    response = db_update_user_role(user_id,role, session)
    return response
