from pydantic import BaseModel, EmailStr
from datetime import datetime



class UserPatch(BaseModel):
    currency:str|None = None
    language:str|None = None


class UserRegister(BaseModel):
    email: EmailStr
    password:str
    password_again:str
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
    money: float
    created_at: datetime
    currency:str
    language:str




