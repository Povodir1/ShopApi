from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime

class UserPatch(BaseModel):
    name: str | None
    password_hash: str | None


class UserRegister(BaseModel):
    name:str
    email: EmailStr
    password_hash:str


class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    money: condecimal(max_digits=10, decimal_places=2)
    role: str
    created_at: datetime

    class Config:
        from_attributes = True




