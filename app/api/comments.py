from fastapi import APIRouter, HTTPException,status
from app.services.comments import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.schemas.comment import CommentUpdateSchema,CommentCreateSchema
router = APIRouter(prefix="/comments",tags=["Comments"])


@router.get("/{item_id}")
def get_comments(item_id:int):
    response = serv_get_comments(item_id)
    return response

@router.patch("/{item_id}")
def patch_comments(item_id:int, user_id:int,new_data:CommentUpdateSchema):
    try:
        response = serv_patch_comment(item_id,user_id,new_data)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")

@router.delete("/{item_id}")
def delete_comments(item_id:int, user_id:int):
    try:
        serv_delete_comment(item_id, user_id)
        return {"msg": "Comment deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")

@router.post("/{item_id}")
def post_comments(new_com:CommentCreateSchema):
    try:
        response = serv_create_comment(new_com)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")







