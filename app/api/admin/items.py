from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends,Form,File, UploadFile

from app.services.api_crud.item import create_item,serv_delete_item, serv_patch_item
from app.schemas.item import ItemCreateSchema,ItemPatchSchema,ItemSoloSchema,AttributeData
from app.schemas.image import ImageSchema
from app.services.security import is_admin
import json

router = APIRouter(prefix="/items",tags=["Items"],dependencies=[Depends(is_admin)])



@router.post("/create",response_model=ItemSoloSchema,status_code=status.HTTP_201_CREATED)
async def post_item(name: str = Form(...),
    price: float = Form(...),
    info: str|None = Form(None),
    images: list[UploadFile] | None = File(None),
    image_metadata: str|None= Form(None),
    stock: int = Form(0),
    attributes: str = Form(...),
    tags: str = Form(...),
    category_id:int = Form(...)):
    try:

        new_item = ItemCreateSchema(name = name,price = price,info = info,
                                    stock = stock,attributes = json.loads(attributes),
                                    image_metadata = json.loads(image_metadata) if image_metadata else None ,
                                    tags =json.loads(tags) ,category_id = category_id)
        response = await create_item(new_item,images)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{item_id}",response_model=ItemSoloSchema)
async def patch_item( item_id:int|None,
                name: str = Form(None),
                price: Optional[float]= Form(None,),
                info: str|None = Form(None),
                images: list[UploadFile] | None = File(None),
                image_metadata: str | None = Form(None),
                stock: int|None = Form(None),
                attributes: str|None = Form(None),
                tags: str | None = Form(None),
                is_active:Optional[bool]= Form(None),
                category_id:int |None = Form(None)):

        new_data = ItemPatchSchema(name = name,price = price,info = info,is_active = is_active,
                                    stock = stock,attributes = json.loads(attributes) if attributes else None,
                                    image_metadata = json.loads(image_metadata) if image_metadata else None,
                                    tags = json.loads(tags) if tags else None,category_id = category_id)
        response = await serv_patch_item(item_id,new_data,images)
        return response



@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id):
    try:
        serv_delete_item(item_id)
        return {"msg:":"Item deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )