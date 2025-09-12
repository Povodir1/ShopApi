from fastapi import APIRouter,HTTPException,status
from app.services.item import get_item, get_all_items, create_item
from app.schemas.item import ItemCreateSchema

router = APIRouter(prefix="/items",tags=["Items"])


@router.get("/all")
def get_item_all(limit:int):
    return get_all_items(limit)


@router.get("/{item_id}")
def get_item(item_id):
    response = get_item(item_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Item with id = {item_id} not found")
    return response


@router.post("/create")
def post_item(new_item: ItemCreateSchema):
    return create_item(new_item)



@router.patch("/{item_id}")
def patch_item(item_id):
    pass


@router.delete("/{item_id}")
def delete_item(item_id):
    pass
