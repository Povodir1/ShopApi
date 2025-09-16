from http.client import responses

from fastapi import APIRouter,HTTPException,status
from app.services.item import serv_get_item, get_all_items, create_item,serv_delete_item, serv_patch_item,serv_get_categories
from app.schemas.item import ItemCreateSchema,ItemPatchSchema

router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all")
def get_item_all(limit:int):
    response = get_all_items(limit)
    return response

@router.get("/category")
def get_categories():
    response = serv_get_categories()
    return response

@router.get("/{item_id}")
def get_item(item_id):
    response = serv_get_item(item_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return response


@router.post("/create")
def post_item(new_item: ItemCreateSchema):
    response = create_item(new_item)
    return response



@router.patch("/{item_id}")
def patch_item(item_id:int,new_data: ItemPatchSchema):
    response = serv_patch_item(item_id,new_data)
    return response


@router.delete("/{item_id}")
def delete_item(item_id):
    response = serv_delete_item(item_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return {"msg":"Item deleted"}

