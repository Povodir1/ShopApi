
from pydantic import BaseModel, condecimal, Field


class OrderItemSchema(BaseModel):
    item_id: int
    item_name:str
    item_image: str| None = None
    count: int = Field(ge=0)
    item_price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        from_attributes = True