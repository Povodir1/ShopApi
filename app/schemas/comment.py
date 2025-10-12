from pydantic import BaseModel,Field
from fastapi import Form
from typing import Optional, Annotated
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
    message: Optional[str] = None
    rating:Optional[float] = Field(default=None,ge=1,le=5)


class CommentCreateSchema(BaseModel):
    item_id: int
    message: Optional[str] = None
    rating: float = Field(ge=1, le=5)