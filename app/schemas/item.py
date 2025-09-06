from pydantic import BaseModel, condecimal
from typing import Optional


class ItemSchema(BaseModel):
    id: int
    name: str
    price: condecimal(max_digits=10, decimal_places=2)
    info: Optional[str]
    image_id: int
    stock: int
    category_id: int

    class Config:
        orm_mode = True