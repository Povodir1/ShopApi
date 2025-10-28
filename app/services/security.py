import datetime
import random
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException
from app.schemas.user import UserTokenDataSchema, UserSchema
from passlib.context import CryptContext
from app.config import settings
from pydantic import EmailStr
from app.models.user import User
from app.exceptions import ObjectNotFoundError,InvalidDataError
from app.database import refresh_token_client,access_blacklist_client
import json
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_auth = OAuth2PasswordBearer(tokenUrl="/login")

def get_token(token:str = Depends(user_auth)):
    if access_blacklist_client.exists(token):
        raise InvalidDataError("Invalid token")
    return decode_token(token)

def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hash_password:str):
    return pwd_context.verify(password,hash_password)

def create_access_token(data:UserTokenDataSchema):
    to_encode = data.model_copy().model_dump()
    to_encode["type"] = "access"
    token = jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=ALGORITHM)
    if access_blacklist_client.exists(token):
        access_blacklist_client.delete(token)
    return token

def create_refresh_token(user_id:int):
    to_encode = {"type": "refresh","id":user_id}
    token = jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=ALGORITHM)
    if refresh_token_client.exists(user_id):
        refresh_token_client.delete(user_id)
    refresh_token_client.setex(user_id,604800,token)
    return token

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
        raise ObjectNotFoundError("Нет пользователя с таким email")
    if not verify_pass(password,user.password_hash):
        raise InvalidDataError("Неверный пароль")
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

def is_correct_pass(password:str):
    if len(password)<8:
        raise InvalidDataError("слишком коротко")
    if password == password.lower():
        raise InvalidDataError("нужны загланые буквы")
    return password


def code_ver(data:dict,code):
    stored_code = data.get("code")
    if str(stored_code) != str(code):
        raise InvalidDataError("неверный код подтверждения")

def update_access_token(refresh_token:str,session):
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    except:
        raise InvalidDataError("Invalid token")
    if payload["type"] != "refresh":
        raise InvalidDataError("Invalid token type")
    if not refresh_token_client.exists(payload["id"]):
        raise ObjectNotFoundError("Token not found")
    if not refresh_token_client[payload["id"]] == refresh_token:
        raise InvalidDataError("Invalid token")
    user = session.query(User).filter(User.id == payload["id"]).first()
    new_token = create_access_token(UserTokenDataSchema(id = user.id,name=user.name,
                                                 role = user.role,currency=user.currency,
                                                 language=user.language))
    return new_token

def block_access_token(token:str):
    #для ttl payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    access_blacklist_client[token] = ""


def block_refresh_token(user_id:int):
    if not refresh_token_client.exists(user_id):
        raise ObjectNotFoundError("Token not found")
    refresh_token_client.delete(user_id)

def create_code(email:EmailStr,
                redis_db,
                ttl,
                new_data:dict|None = None
                ):
    if not new_data:
        new_data = {}
    code = access_code()
    new_data["code"] = code
    new_data["try_counts"] = 3
    data = new_data
    data_json = json.dumps(data)
    if redis_db.exists(email):
        redis_db.delete(email)
    redis_db.setex(email, ttl, data_json)
    return code