from typing import Optional

from fastapi import APIRouter, status, Depends, UploadFile, File, Form, Path
from app.services.api_crud.comments import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.services.security import get_token
from app.schemas.comment import CommentUpdateSchema,CommentCreateSchema,CommentSchema
from app.schemas.user import UserTokenDataSchema
from app.database import get_session
from sqlalchemy.orm.session import Session
from app.services.api_crud.comments import SortType

router = APIRouter(prefix="/comments",tags=["Comments"])


@router.get("/{item_id}",response_model=list[CommentSchema])
def get_comments(item_id:int,
                 sort_type:SortType = SortType.by_date,
                 session:Session = Depends(get_session)
                 ):
    response = serv_get_comments(item_id,sort_type,session)
    return response

@router.patch("/{item_id}",response_model=CommentSchema)
async def patch_comments(item_id:int,
                         message: Optional[str] = Form(None),
                         rating: float = Form(...),
                         media: Optional[list[UploadFile]] = File(None),
                         user: UserTokenDataSchema = Depends(get_token),
                         session:Session = Depends(get_session)
                         ):
        new_data = CommentUpdateSchema(message=message, rating=rating)
        response = await serv_patch_comment(item_id,user.id,new_data,media,session)
        return response


@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_comments(item_id:int,
                    user: UserTokenDataSchema = Depends(get_token),
                    session:Session = Depends(get_session)
                    ):
    serv_delete_comment(item_id, user.id,session)
    return {"msg": "Comment deleted"}


@router.post("/{item_id}",response_model=CommentSchema,status_code=status.HTTP_201_CREATED)
async def post_comments(item_id: int = Path(),
                        message: Optional[str] = Form(None),
                        rating: float = Form(...),
                        media: Optional[list[UploadFile]] = File(None),
                        user: UserTokenDataSchema = Depends(get_token),
                        session:Session = Depends(get_session)
                        ):
        new_com = CommentCreateSchema(item_id = item_id, message= message,rating=rating)
        response = await serv_create_comment(new_com,user.id,media,session)
        return response




