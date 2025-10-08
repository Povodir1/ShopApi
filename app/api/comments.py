from fastapi import APIRouter, HTTPException,status,Depends
from app.services.comments import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.services.security import get_token
from app.schemas.comment import CommentUpdateSchema,CommentCreateSchema,CommentSchema
from app.schemas.user import UserSchema, UserTokenDataSchema
router = APIRouter(prefix="/comments",tags=["Comments"])


@router.get("/{item_id}",response_model=list[CommentSchema])
def get_comments(item_id:int):
    response = serv_get_comments(item_id)
    return response

@router.patch("/{item_id}",response_model=CommentSchema)
def patch_comments(item_id:int,new_data:CommentUpdateSchema, user: UserTokenDataSchema = Depends(get_token)):

        response = serv_patch_comment(item_id,user.id,new_data)
        return response


@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_comments(item_id:int, user: UserTokenDataSchema = Depends(get_token)):
    try:
        serv_delete_comment(item_id, user.id)
        return {"msg": "Comment deleted"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")

@router.post("/{item_id}",response_model=CommentSchema,status_code=status.HTTP_201_CREATED)
def post_comments(new_com:CommentCreateSchema,user: UserTokenDataSchema = Depends(get_token)):
    try:
        response = serv_create_comment(new_com,user.id)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")







