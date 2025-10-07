
from app.database import db_session
from app.models.user import User
from app.schemas.user import UserSchema, UserRegister, UserPatch,UserTokenDataSchema
from pydantic import EmailStr
from app.services.security import verify_pass, hash_pass
from app.models.user import CurrencyType,LanguageList


def is_unique_email(email:EmailStr):
    with db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        return False if user else True


def user_by_email_pass(email:str|EmailStr,password:str):
    with db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise ValueError("Нет пользователя с таким email")
        if not verify_pass(password,user.password_hash):
            raise ValueError("Неверный пароль")
        return UserTokenDataSchema(id = user.id,name = user.name,role = user.role,currency=user.currency.name,language=user.language.name)

def get_user(user_id):
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Нет пользователя с таким id")
        return UserSchema.model_validate(user)

def create_user(user_data: UserRegister):
    user = User(**user_data.model_dump())
    user.password_hash = hash_pass(user_data.password_hash  )
    with db_session() as session:
        session.add(user)
        session.flush()
        return UserSchema.model_validate(user)

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

def reset_password(email:EmailStr|str,new_password):
    with db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        user.password_hash = hash_pass(new_password)
        session.flush()
        return UserSchema.model_validate(user,from_attributes=True)

