from pydantic import BaseModel, condecimal, Field
from typing import Optional
from app.schemas.image import ImageSchema

class ItemCatalogSchema(BaseModel):
    id: int
    name: str
    images: str | None = None
    price: float = 0
    rating: float | None = None

    class Config:
        from_attributes = True

class ItemSoloSchema(ItemCatalogSchema):
    info: Optional[str] = None
    images: list[ImageSchema] | None = None
    stock: int = Field(ge=0)

class ItemCreateSchema(BaseModel):
    name: str
    price: float = 0
    info: Optional[str] = None
    stock: int = Field(ge=0)
    category_id:int = None

    class Config:
        from_attributes = True

class ItemPatchSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    info: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True


