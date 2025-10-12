from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Path
from app.services.api_crud.comments import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.services.security import get_token
from app.schemas.comment import CommentUpdateSchema,CommentCreateSchema,CommentSchema
from app.schemas.user import UserTokenDataSchema
router = APIRouter(prefix="/comments",tags=["Comments"])


@router.get("/{item_id}",response_model=list[CommentSchema])
def get_comments(item_id:int):
    response = serv_get_comments(item_id)
    return response

@router.patch("/{item_id}",response_model=CommentSchema)
async def patch_comments(item_id:int,
                   message: Optional[str] = Form(None),
                   rating: float = Form(...),
                   media: Optional[list[UploadFile]] = File(None),
                   user: UserTokenDataSchema = Depends(get_token)):
        new_data = CommentUpdateSchema(message=message, rating=rating)
        response = await serv_patch_comment(item_id,user.id,new_data,media)
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
async def post_comments(
        item_id: int = Path(),
        message: Optional[str] = Form(None),
        rating: float = Form(...),
        media: Optional[list[UploadFile]] = File(None),
        user: UserTokenDataSchema = Depends(get_token)
):
    try:
        new_com = CommentCreateSchema(item_id = item_id, message= message,rating=rating)
        response = await serv_create_comment(new_com,user.id,media)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}")







