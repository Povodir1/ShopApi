from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class CommentSchema(BaseModel):
    username: str
    message: Optional[str]
    rating: Optional[int] = Field(ge=1,le=5)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True