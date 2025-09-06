
from pydantic import BaseModel, condecimal

class OrderItemSchema(BaseModel):
    id: int
    item_id: int
    order_id: int
    count: int
    item_price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True