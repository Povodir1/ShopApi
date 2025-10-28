from fastapi import APIRouter, Depends
from app.services.api_crud.user import get_user,patch_user
from app.schemas.user import UserPatch,UserSchema,UserTokenDataSchema
from app.services.security import get_token,check_permissions
from app.database import get_session,Session
from app.models.user import CurrencyType,LanguageList
from app.models.permission import ResourceEnum as Res, ActionEnum as Act


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema)
def get_user_me(user:UserTokenDataSchema = Depends(get_token),
                perm = Depends(check_permissions(Res.USERS,Act.READ)),
                session:Session = Depends(get_session)
                ):
    response = get_user(user.id,session)
    return response


@router.patch("/me",response_model=UserSchema)
def patch_user_me(currency:CurrencyType|None = None,
                  language:LanguageList|None = None,
                  user: UserTokenDataSchema = Depends(get_token),
                  perm = Depends(check_permissions(Res.USERS,Act.UPDATE)),
                  session:Session = Depends(get_session)
                  ):
    user_data = UserPatch(currency = currency.value if currency else None,
                          language=language.value if language else None)
    response = patch_user(user.id,user_data,session)
    return response
