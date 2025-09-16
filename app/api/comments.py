from fastapi import APIRouter, HTTPException,status
from app.services.comments import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.schemas.comment import CommentUpdateSchema,CommentCreateSchema
router = APIRouter(prefix="/comments",tags=["Comments"])

#юзер по токену

@router.get("/{item_id}")
def get_comments(item_id:int):
    response = serv_get_comments(item_id)
    return response

@router.patch("/{item_id}")
def patch_comments(item_id:int, user_id:int,new_data:CommentUpdateSchema):
    response = serv_patch_comment(item_id,user_id,new_data)
    return response

@router.delete("/{item_id}")
def delete_comments(item_id:int, user_id:int):
    response = serv_delete_comment(item_id, user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return {"msg": "Comment deleted"}

@router.post("/{item_id}")
def post_comments(new_com:CommentCreateSchema):
    response = serv_create_comment(new_com)
    return response







