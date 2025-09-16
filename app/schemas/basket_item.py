from pydantic import BaseModel,Field
from app.schemas.image import ImageOneSchema

class BasketItemSchema(BaseModel):
    id: int
    item_id:int
    item_name:str
    images: ImageOneSchema | None = None
    count: int = Field(ge=1)
    full_price: float
    rating: float | None = None

    class Config:
        from_attributes = True