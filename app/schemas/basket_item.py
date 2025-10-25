from pydantic import BaseModel,Field


class BasketItemSchema(BaseModel):
    id: int
    item_id:int
    item_name:str
    images: str | None = None
    count: int = Field(ge=1)
    full_price: float
    rating: float | None = None

    class Config:
        from_attributes = True

class BasketSchema(BaseModel):
    items: list[BasketItemSchema]
    full_price:float