from app.database import db_session
from app.schemas.user import UserSchema, UserRegister, UserPatch
from app.services.security import  hash_pass
from app.models.user import User,CurrencyType,LanguageList,Role


def get_user(user_id):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Нет пользователя с таким id")
        return UserSchema.model_validate(user,from_attributes=True)

def create_user(user_data: UserRegister):
    user = User(**user_data.model_dump())
    user.password_hash = hash_pass(user_data.password_hash  )
    with db_session() as session:
        session.add(user)
        session.flush()
        return UserSchema.model_validate(user,from_attributes=True)

def patch_user(user_id:int, new_data:UserPatch):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Нет пользователя с таким id")
        if new_data.currency not in [i.name for i in CurrencyType] and new_data.currency is not None:
            raise ValueError("Неверная валюта")
        if new_data.language not in [i.name for i in LanguageList] and new_data.language is not None:
            raise ValueError("Неверный язык")
        for key,value in new_data.model_dump(exclude_none=True).items():
            setattr(user,key,value)
        session.flush()
        return UserSchema.model_validate(user,from_attributes=True)

def change_role(user_id:int,role: Role):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User не найден")
        user.role = role
        return UserSchema.model_validate(user,from_attributes=True)


def ban_user(user_id:int,is_banned:bool = True):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User не найден")
        user.is_banned = is_banned
        return UserSchema.model_validate(user,from_attributes=True)

