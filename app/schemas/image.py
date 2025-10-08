from pydantic import BaseModel

class ImageSchema(BaseModel):
    is_main: bool
    url: str
    class Config:
        from_attributes = True