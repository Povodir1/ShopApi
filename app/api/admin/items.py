from fastapi import APIRouter, HTTPException, status, Depends

from app.services.api_crud.item import create_item,serv_delete_item, serv_patch_item
from app.schemas.item import ItemCreateSchema,ItemPatchSchema,ItemSoloSchema
from app.services.security import is_admin

router = APIRouter(prefix="/items",tags=["Items"],dependencies=[Depends(is_admin)])



@router.post("/create",response_model=ItemSoloSchema,status_code=status.HTTP_201_CREATED)
def post_item(new_item: ItemCreateSchema):
    try:
        response = create_item(new_item)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{item_id}",response_model=ItemSoloSchema)
def patch_item(item_id:int,new_data: ItemPatchSchema):
    try:
        response = serv_patch_item(item_id,new_data)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


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