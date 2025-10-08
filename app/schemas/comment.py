from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class CommentMediaSchema(BaseModel):
    url:str
    type:str

class CommentSchema(BaseModel):
    id:int
    username: str
    media: Optional[list[CommentMediaSchema]]
    message: Optional[str]
    rating: float = Field(ge=1,le=5)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentUpdateSchema(BaseModel):
    media: Optional[list[CommentMediaSchema]] = None
    message: Optional[str] = None

class CommentCreateSchema(BaseModel):
    item_id:int
    media: Optional[list[CommentMediaSchema]]
    message: Optional[str] = None
    rating: float = Field(ge=1,le=5)