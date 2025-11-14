from app.api.users.schemas import UserSchema, UserRegister, UserPatch

from app.core.security import  hash_pass
from app.core.exceptions import ObjectNotFoundError,InvalidDataError

from app.models.user import User,CurrencyType,LanguageList



def get_user(user_id:int,session):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким id")
    return UserSchema(id = user.id,name= user.name,role = user.roles.name,
                      email = user.email, money = user.money,created_at=user.created_at,
                      currency=user.currency,language=user.language)

def create_user(user_data: UserRegister,session):
    user = User(name = user_data.name,email = user_data.email)
    user.password_hash = hash_pass(user_data.password)
    session.add(user)
    session.flush()
    return UserSchema(id = user.id,name= user.name,role = user.roles.name,
                      email = user.email, money = user.money,created_at=user.created_at,
                      currency=user.currency,language=user.language)

def patch_user(user_id:int, new_data:UserPatch,session):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ObjectNotFoundError("Нет пользователя с таким id")
    if new_data.currency not in [i.name for i in CurrencyType] and new_data.currency is not None:
        raise InvalidDataError("Неверная валюта")
    if new_data.language not in [i.name for i in LanguageList] and new_data.language is not None:
        raise InvalidDataError("Неверный язык")
    for key,value in new_data.model_dump(exclude_none=True).items():
        setattr(user,key,value)
    session.flush()
    return UserSchema(id = user.id,name= user.name,role = user.roles.name,
                      email = user.email, money = user.money,created_at=user.created_at,
                      currency=user.currency,language=user.language)


def ban_user(user_id:int,is_banned:bool,session):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ObjectNotFoundError("User не найден")
    user.is_banned = is_banned
    return UserSchema(id = user.id,name= user.name,role = user.roles.name,
                      email = user.email, money = user.money,created_at=user.created_at,
                      currency=user.currency,language=user.language)
