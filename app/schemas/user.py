from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime
from typing import Optional
from app.models.user import CurrencyType
#old
class UserPatch(BaseModel):
    name: Optional[str] = None
    password_hash: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password_hash:str


class UserRegister(UserLogin):
    name:str


class UserTokenDataSchema(BaseModel):
    id: int
    name: str
    role: str
    currency:str
    language:str



class UserSchema(BaseModel):
    id: int
    name: str
    role: str
    email: EmailStr
    money: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime





