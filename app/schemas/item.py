from pydantic import BaseModel, condecimal, Field
from typing import Optional


class ItemSchema(BaseModel):
    id: int
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    info: Optional[str]
    image_id: int
    stock: int = Field(ge=0)
    category_id: int

    class Config:
        from_attributes = True