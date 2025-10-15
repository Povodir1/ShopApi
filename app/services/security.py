import datetime
import random
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from app.schemas.user import UserTokenDataSchema, UserSchema
from passlib.context import CryptContext
from app.config import settings
from pydantic import EmailStr
from app.database import db_session
from app.models.user import User

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_auth = OAuth2PasswordBearer(tokenUrl="/token")
user_auth_optional = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

def get_token(token:str = Depends(user_auth)):
    return decode_token(token)

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hash_password:str):
    return pwd_context.verify(password,hash_password)

def create_token(data:UserTokenDataSchema):
    to_encode = data.model_copy()
    return jwt.encode(to_encode.model_dump(),settings.JWT_SECRET_KEY,algorithm=ALGORITHM)

def decode_token(token:str):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    return UserTokenDataSchema(**payload)


def access_code():
    return str(random.randint(100000,999999))



def is_unique_email(email:EmailStr,session):
    user = session.query(User).filter(User.email == email).first()
    return False if user else True


def user_by_email_pass(email:str|EmailStr,password:str,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Нет пользователя с таким email")
    if not verify_pass(password,user.password_hash):
        raise ValueError("Неверный пароль")
    user.last_login = datetime.datetime.now()
    return UserTokenDataSchema(id = user.id,name = user.name,role = user.role,currency=user.currency.name,language=user.language.name)


def reset_password(email:EmailStr|str,new_password,session):
    user = session.query(User).filter(User.email == email).first()
    user.password_hash = hash_pass(new_password)
    session.flush()
    return UserSchema.model_validate(user,from_attributes=True)

def is_admin(user:UserTokenDataSchema = Depends(get_token)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Вы не админ")
    return user
