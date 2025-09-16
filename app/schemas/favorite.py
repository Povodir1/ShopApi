from pydantic import BaseModel
from app.schemas.image import ImageOneSchema
class FavouriteItemSchema(BaseModel):
    id: int
    item_id: int
    item_name: str
    images: ImageOneSchema | None = None
    rating: float | None = None

    class Config:
        from_attributes = True