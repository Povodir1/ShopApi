from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    url: str
    is_main: bool
    item_id: int

    class Config:
        from_attributes = True