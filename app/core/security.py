import random
from passlib.context import CryptContext
from pydantic import EmailStr
import json

from app.core.exceptions import InvalidDataError



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#засолить
def hash_pass(password:str):
    return pwd_context.hash(password)

def verify_pass(password:str,hash_password:str):
    return pwd_context.verify(password,hash_password)


def is_correct_pass(password:str):
    if len(password)<8:
        raise InvalidDataError("слишком коротко")
    if password == password.lower():
        raise InvalidDataError("нужны загланые буквы")
    return password


def access_code():
    return str(random.randint(100000,999999))

def code_ver(data:dict,code):
    stored_code = data.get("code")
    if str(stored_code) != str(code):
        raise InvalidDataError("неверный код подтверждения")

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
