from pydantic import BaseModel



class ImageOneSchema(BaseModel):
    url: str
    class Config:
        from_attributes = True


class ImageSchema(ImageOneSchema):
    is_main: bool

