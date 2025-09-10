from pydantic import BaseModel, condecimal, Field
from typing import Optional
from app.schemas.image import ImageSchema

class ItemCatalogSchema(BaseModel):
    id: int
    name: str
    images: ImageSchema | None = None
    price: condecimal(max_digits=10, decimal_places=2)
    rating: float | None

    class Config:
        from_attributes = True

class ItemSoloSchema(ItemCatalogSchema):
    info: Optional[str]
    images: list[ImageSchema] | None = None
    stock: int = Field(ge=0)
