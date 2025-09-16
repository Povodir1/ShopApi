from pydantic import BaseModel

class FavouriteItemSchema(BaseModel):
    id: int
    user_id: int
    item_id: int

    class Config:
        from_attributes = True