
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.api.users.schemas import UserTokenDataSchema
from app.core.config import settings
from app.models.user import User
from app.core.exceptions import ObjectNotFoundError,InvalidDataError
from app.core.database import refresh_token_client,access_blacklist_client

ALGORITHM = "HS256"
user_auth = OAuth2PasswordBearer(tokenUrl="/login")

def get_token(token:str = Depends(user_auth)):
    if access_blacklist_client.exists(token):
        raise InvalidDataError("Invalid token")
    return decode_token(token)

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
                                                 role = user.roles.name,currency=user.currency,
                                                 language=user.language))
    return new_token

def block_access_token(token:str):
    #для ttl payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=ALGORITHM)
    access_blacklist_client[token] = ""


def block_refresh_token(user_id:int):
    if not refresh_token_client.exists(user_id):
        raise ObjectNotFoundError("Token not found")
    refresh_token_client.delete(user_id)
