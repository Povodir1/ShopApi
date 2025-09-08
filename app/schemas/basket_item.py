from pydantic import BaseModel,Field


class BasketItemSchema(BaseModel):
    id: int
    user_id: int
    item_id: int
    count: int = Field(ge=0)

    class Config:
        from_attributes = True