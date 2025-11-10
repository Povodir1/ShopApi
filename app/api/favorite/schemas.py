from pydantic import BaseModel
class FavouriteItemSchema(BaseModel):
    id: int
    item_id: int
    item_name: str
    images: str | None = None
    rating: float | None = None

    class Config:
        from_attributes = True