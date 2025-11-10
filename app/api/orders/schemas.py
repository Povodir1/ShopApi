from datetime import datetime
from pydantic import BaseModel, condecimal, Field


class OrderItemSchema(BaseModel):
    item_id: int
    item_name:str
    item_image: str| None = None
    count: int = Field(ge=0)
    item_price: float

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: int
    items: list[OrderItemSchema]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    price: float
    status: str = "pending"

    class Config:
        from_attributes = True