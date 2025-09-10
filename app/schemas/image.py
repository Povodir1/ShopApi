from pydantic import BaseModel


class ImageSchema(BaseModel):
    id: int
    url: str
    is_main: bool

    class Config:
        from_attributes = True