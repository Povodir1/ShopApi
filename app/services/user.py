
from app.database import db_session
from app.models.user import User
from app.schemas.user import UserSchema, UserRegister, UserPatch,UserToken
from pydantic import EmailStr
from app.services.security import verify_pass, hash_pass, decode_token, user_auth_optional,user_auth
from fastapi import Depends


def user_by_token(token:str = Depends(user_auth)):
    data = decode_token(token)
    return UserToken(**data)

def user_by_token_optional(token:str|None = Depends(user_auth_optional)):
    if not token:
        return None
    data = decode_token(token)
    return UserToken(**data)

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
        return UserToken.model_validate(user)

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
    if new_data.password_hash:
        new_data.password_hash = hash_pass(new_data.password_hash)
    with db_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Нет пользователя с таким id")
        for key,value in new_data.model_dump(exclude_none=True).items():
            setattr(user,key,value)
        session.flush()
        return UserSchema.model_validate(user)

def reset_password(email:EmailStr|str,new_password):
    with db_session() as session:
        user = session.query(User).filter(User.email == email).first()
        user.password_hash = hash_pass(new_password)
        session.flush()
        return UserSchema.model_validate(user)



