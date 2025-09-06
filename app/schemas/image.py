from pydantic import BaseModel
from datetime import datetime

class ImageSchema(BaseModel):
    id: int
    url: str
    is_main: bool
    item_id: int
    created_at: datetime

    class Config:
        orm_mode = True