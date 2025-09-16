from pydantic import BaseModel, condecimal
from datetime import datetime
from app.schemas.order_item import OrderItemSchema
class OrderSchema(BaseModel):
    id: int
    items: list[OrderItemSchema]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    price: condecimal(max_digits=10, decimal_places=2)
    status: str = "pending"

    class Config:
        from_attributes = True