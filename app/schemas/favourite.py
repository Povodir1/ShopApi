from pydantic import BaseModel

class FavouriteItemSchema(BaseModel):
    id: int
    user_id: int
    item_id: int

    class Config:
        orm_mode = True