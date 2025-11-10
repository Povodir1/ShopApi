from fastapi import APIRouter, Depends
from app.api.users.services import get_user,patch_user
from app.api.users.schemas import UserPatch,UserSchema,UserTokenDataSchema
from app.core.dependencies import get_token,check_permissions
from app.core.database import get_session,Session
from app.models.user import CurrencyType,LanguageList
from app.models.permission import ResourceEnum as Res, ActionEnum as Act

from app.api.users.services import change_role,ban_user


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema,dependencies=[Depends(check_permissions(Res.USERS,Act.READ))])
def get_user_me(user:UserTokenDataSchema = Depends(get_token),
                session:Session = Depends(get_session)
                ):
    response = get_user(user.id,session)
    return response


@router.patch("/me",response_model=UserSchema,dependencies=[Depends(check_permissions(Res.USERS,Act.UPDATE))])
def patch_user_me(currency:CurrencyType|None = None,
                  language:LanguageList|None = None,
                  user: UserTokenDataSchema = Depends(get_token),
                  session:Session = Depends(get_session)
                  ):
    user_data = UserPatch(currency = currency.value if currency else None,
                          language=language.value if language else None)
    response = patch_user(user.id,user_data,session)
    return response

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


