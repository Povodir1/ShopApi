from pydantic import BaseModel


class BasketItemSchema(BaseModel):
    id: int
    user_id: int
    item_id: int
    count: int

    class Config:
        orm_mode = True