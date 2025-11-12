from typing import Optional
from fastapi import APIRouter, status, Depends, UploadFile, File, Form, Path

from app.api.comments.services import serv_get_comments,serv_patch_comment,serv_delete_comment,serv_create_comment
from app.api.comments.schemas import CommentUpdateSchema,CommentCreateSchema,CommentSchema,CommentsViewSchema
from app.api.comments.services import SortType

from app.core.dependencies import TokenDep,check_permissions,SessionDep

from app.models.permission import ResourceEnum as Res, ActionEnum as Act


router = APIRouter(prefix="/comments",tags=["Comments"])


@router.get("/{item_id}",response_model=CommentsViewSchema,
            dependencies=[Depends(check_permissions(Res.COMMENTS, Act.READ))])
def get_comments(item_id:int,
                 session: SessionDep,
                 limit:int = 10,
                 page:int = 1,
                 sort_type:SortType = SortType.by_date,
                 ):
    response = serv_get_comments(item_id,limit,page,sort_type,session)
    return response

@router.patch("/{item_id}",response_model=CommentSchema,
              dependencies=[Depends(check_permissions(Res.COMMENTS, Act.UPDATE))])
async def patch_comments(item_id:int,
                         user: TokenDep,
                         session: SessionDep,
                         message: Optional[str] = Form(None),
                         rating: float = Form(...),
                         media: Optional[list[UploadFile]] = File(None),
                         ):
        new_data = CommentUpdateSchema(message=message, rating=rating)
        response = await serv_patch_comment(item_id,user.id,new_data,media,session)
        return response


@router.delete("/{item_id}",status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(check_permissions(Res.COMMENTS, Act.DELETE))])
def delete_comments(item_id:int,
                    user: TokenDep,
                    session:SessionDep
                    ):
    serv_delete_comment(item_id, user.id,session)
    return {"msg": "Comment deleted"}


@router.post("/{item_id}",response_model=CommentSchema,status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(check_permissions(Res.COMMENTS, Act.CREATE))])
async def post_comments(user: TokenDep,
                        session:SessionDep,
                        item_id: int = Path(),
                        message: Optional[str] = Form(None),
                        rating: float = Form(...),
                        media: Optional[list[UploadFile]] = File(None),
                        ):
        new_com = CommentCreateSchema(item_id = item_id, message= message,rating=rating)
        response = await serv_create_comment(new_com,user.id,media,session)
        return response




