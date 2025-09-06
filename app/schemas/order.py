from pydantic import BaseModel, condecimal
from datetime import datetime

class OrderSchema(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    price: condecimal(max_digits=10, decimal_places=2)
    status: str

    class Config:
        orm_mode = True