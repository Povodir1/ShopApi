from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends,Form,File, UploadFile

from app.services.api_crud.item import create_item,serv_delete_item, serv_patch_item
from app.schemas.item import ItemCreateSchema,ItemPatchSchema,ItemSoloSchema
from app.services.security import is_admin
import json
from app.database import get_session
from sqlalchemy.orm.session import Session
router = APIRouter(prefix="/items",tags=["Items"],dependencies=[Depends(is_admin)])



@router.post("/create",response_model=ItemSoloSchema,status_code=status.HTTP_201_CREATED)
def post_item(name: str = Form(...),
    price: float = Form(...),
    info: str|None = Form(None),
    images: list[UploadFile] | None = File(None),
    image_metadata: str|None= Form(None),
    stock: int = Form(0),
    attributes: str = Form(...),
    tags: str = Form(...),
    category_id:int = Form(...),
    session:Session = Depends(get_session)):
    try:
        new_item = ItemCreateSchema(name = name,price = price,info = info,
                                    stock = stock,attributes = json.loads(attributes),
                                    image_metadata = json.loads(image_metadata) if image_metadata else None ,
                                    tags =json.loads(tags) ,category_id = category_id)
        response = create_item(new_item,images,session)
        return response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{item_id}",response_model=ItemSoloSchema)
def patch_item( item_id:int|None,
                name: str = Form(None),
                price: Optional[float]= Form(None,),
                info: str|None = Form(None),
                images: list[UploadFile] | None = File(None),
                image_metadata: str | None = Form(None),
                stock: int|None = Form(None),
                attributes: str|None = Form(None),
                tags: str | None = Form(None),
                is_active:Optional[bool]= Form(None),
                category_id:int |None = Form(None),
                session:Session = Depends(get_session)):

        new_data = ItemPatchSchema(name = name,price = price,info = info,is_active = is_active,
                                    stock = stock,attributes = json.loads(attributes) if attributes else None,
                                    image_metadata = json.loads(image_metadata) if image_metadata else None,
                                    tags = json.loads(tags) if tags else None,category_id = category_id)
        response = serv_patch_item(item_id,new_data,images,session)
        return response



@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id,session:Session = Depends(get_session)):
    try:
        serv_delete_item(item_id,session)
        return {"msg:":"Item deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )