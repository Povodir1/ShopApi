from fastapi import APIRouter, Depends

from app.api.users.services import get_user,patch_user
from app.api.users.schemas import UserPatch,UserSchema
from app.api.users.services import ban_user

from app.core.dependencies import check_permissions,TokenDep,SessionDep

from app.models.user import CurrencyType,LanguageList
from app.core.enums import ResourceEnum as Res, ActionEnum as Act



router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema,dependencies=[Depends(check_permissions(Res.USERS,Act.READ))])
def get_user_me(user: TokenDep,
                session:SessionDep
                ):
    response = get_user(user.id,session)
    return response


@router.patch("/me",response_model=UserSchema,dependencies=[Depends(check_permissions(Res.USERS,Act.UPDATE))])
def patch_user_me(user: TokenDep,
                  session:SessionDep,
                  currency:CurrencyType|None = None,
                  language:LanguageList|None = None,

                  ):
    user_data = UserPatch(currency = currency.value if currency else None,
                          language=language.value if language else None)
    response = patch_user(user.id,user_data,session)
    return response

@router.patch("/ban",
              tags=["Admin"],
              dependencies=[Depends(check_permissions(Res.USERS, Act.DELETE))])
def ban_user(user_id:int,
             session:SessionDep,
             is_banned:bool = True,
             ):
    response = ban_user(user_id,is_banned,session)
    return response


