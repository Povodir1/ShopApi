from typing import Annotated

from fastapi import Depends
from app.api.users.schemas import UserTokenDataSchema
from app.models.permission import Permission,ActionEnum,ResourceEnum
from app.models.role import Role
from app.core.exceptions import NoPermissionsError
from sqlalchemy.orm import Session
from app.core.database import get_session
from .jwt import get_token

def check_permissions(resource:ResourceEnum,
                      action:ActionEnum):
    def wrapped(user:UserTokenDataSchema = Depends(get_token),
               session = Depends(get_session)):
        user_permissions = session.query(Permission).join(Role).filter( Role.name == user.role,
                                                                        Permission.resource == resource.value,
                                                                        Permission.action == action.value).first()
        if not user_permissions:
            raise NoPermissionsError(detail="No permissions")
    return wrapped

token_dependence = Annotated[UserTokenDataSchema,Depends(get_token)]
session_dependence = Annotated[Session,Depends(get_session)]
