import random
import time

from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config import settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_auth = OAuth2PasswordBearer(tokenUrl="/token")

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hash_password:str):
    return pwd_context.verify(password,hash_password)

def create_token(user_data:dict):
    to_encode = user_data.copy()
    return  jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=ALGORITHM)

def decode_token(token:str):
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    return payload


def access_code():
    return str(random.randint(100000,999999))
