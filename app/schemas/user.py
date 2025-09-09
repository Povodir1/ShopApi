from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime


class UserPatch(BaseModel):
    name: str | None
    password_hash: str | None


class UserLogin(BaseModel):
    email: EmailStr
    password_hash:str


class UserRegister(UserLogin):
    name:str


class UserToken(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class UserSchema(UserToken):
    money: condecimal(max_digits=10, decimal_places=2)
    created_at: datetime





