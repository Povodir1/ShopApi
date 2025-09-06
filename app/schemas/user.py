from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    money: condecimal(max_digits=10, decimal_places=2)
    role: str
    created_at: datetime

    class Config:
        orm_mode = True