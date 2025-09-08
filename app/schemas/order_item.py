
from pydantic import BaseModel, condecimal, Field

class OrderItemSchema(BaseModel):
    id: int
    item_id: int
    order_id: int
    count: int = Field(ge=0)
    item_price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True