import datetime

from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.image import ImageSchema
from fastapi import Query



class ItemCatalogSchema(BaseModel):
    id: int
    name: str
    images: str | None = None
    price: float
    rating: float | None = None

    class Config:
        from_attributes = True

class CatalogSchema(BaseModel):
    items:list[ItemCatalogSchema]
    current_page:int
    max_page:int

class AttributeData(BaseModel):
    value:str
    unit:str | None

class ItemSoloSchema(ItemCatalogSchema):
    info: Optional[str] = None
    images: list[ImageSchema] = None
    attributes: list[dict[str,AttributeData]]| None
    stock: int = Field(ge=0)

class ItemCreateSchema(BaseModel):
    name: str
    price: float = 0
    info: str|None = None
    image_metadata: list[bool] | None = None
    stock: int = Field(ge=0)
    attributes: dict[int,AttributeData]
    tags: list[int]
    category_id:int

    class Config:
        from_attributes = True


class ItemPatchSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    image_metadata: list[bool] | None = None
    info: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None
    attributes: Optional[dict[int,AttributeData]] = None
    tags: Optional[list[int]] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True

class ItemFilterSchema(BaseModel):
    min_price: int | None = Field(None, ge=0, description="Минимальная цена")
    max_price: int | None = Field(None, ge=0, description="Максимальная цена")
    category: int | None = Field(None, description="ID категории")

def get_filters(
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    category: int | None = Query(None)
) -> ItemFilterSchema:
    return ItemFilterSchema(
        min_price=min_price,
        max_price=max_price,
        category=category
    )
