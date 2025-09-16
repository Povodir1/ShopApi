from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class CommentSchema(BaseModel):
    id:int
    username: str
    message: Optional[str]
    rating: Optional[int] = Field(ge=1,le=5)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentUpdateSchema(BaseModel):
    message: Optional[str] = None

class CommentCreateSchema(BaseModel):
    user_id:int
    item_id:int
    message: Optional[str] = None
    rating:Optional[float] = None