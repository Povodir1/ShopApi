import random

from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.schemas.user import UserTokenDataSchema
from passlib.context import CryptContext
from app.config import settings

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
