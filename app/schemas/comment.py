from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentSchema(BaseModel):
    id: int
    user_id: int
    item_id: int
    message: Optional[str]
    rating: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True