import datetime
from fastapi import UploadFile
from enum import Enum
from sqlalchemy.orm import joinedload


from app.models import Comment, CommentMedia

from app.api.comments.schemas import CommentSchema, CommentUpdateSchema,CommentCreateSchema,CommentMediaSchema,CommentsViewSchema

from app.core.exceptions import ObjectNotFoundError,ObjectAlreadyExistError
from app.core.config import settings


folder_path = settings.MEDIA_PATH/"comments"


class SortType(Enum):
    by_rating = "rating_desc"
    by_date = "date_desc"

def serv_get_comments(item_id:int,limit_num:int,page:int,sort_type:SortType,session):
    comments_query = session.query(Comment).options(joinedload(Comment.users)).filter(Comment.item_id==item_id)
    if sort_type == SortType.by_date:
        comments_query = comments_query.order_by(Comment.created_at)
    elif sort_type == SortType.by_rating:
        comments_query = comments_query.order_by(Comment.rating.desc())
    comments = comments_query.all()

    comment_list = []
    for comment in comments:
        com_media = [CommentMediaSchema(url = str(folder_path/med.url),type = med.media_type) for med in comment.comment_medias]

        com  = CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                              rating = comment.rating,media=com_media,created_at=comment.created_at,
                              updated_at=comment.updated_at)
        comment_list.append(com)
    max_page = (len(comment_list) // limit_num if len(comment_list) / limit_num == len(comment_list) // limit_num else len(comment_list) // limit_num + 1)
    comment_list = comment_list[(page - 1) * limit_num:(page - 1) * limit_num + limit_num]
    return CommentsViewSchema(comments = comment_list,all_comments_count=len(comments),current_page=page,max_page=max_page)

async def serv_patch_comment(item_id:int,user_id:int,new_data:CommentUpdateSchema,media:list[UploadFile] |None,session):
    comment = session.query(Comment).filter(Comment.user_id ==user_id,Comment.item_id == item_id).first()
    if not comment:
        raise ObjectNotFoundError("Комментарий не найден")
    db_com_medias = []
    com_medias = []
    if media:
        for file in folder_path.iterdir():
            if file.is_file() and f"{comment.id}." in file.name:
                file.unlink()

        for ind, file in enumerate(media):
            file_name = f"{comment.id}.{user_id}.{ind}.{file.filename.split('.')[1]}"
            path = folder_path / file_name
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_com_medias.append(CommentMedia(url=str(file_name), media_type=file.content_type, comment_id=comment.id))
                com_medias.append(CommentMediaSchema(url=str(path), type=file.content_type))

        session.query(CommentMedia).filter(CommentMedia.comment_id == comment.id).delete()
        session.add_all(db_com_medias)


    for key,val in new_data.model_dump(exclude_none=True).items():
        setattr(comment,key,val)
    session.flush()
    comment.updated_at = datetime.datetime.now()
    return CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                         rating = comment.rating,created_at=comment.created_at,
                         updated_at=comment.updated_at,media=com_medias)


async def serv_create_comment(data:CommentCreateSchema,user_id:int,media:list[UploadFile] |None ,session):
    is_available = session.query(Comment).filter(Comment.user_id == user_id,
                                                 Comment.item_id == data.item_id).first()
    if is_available:
        raise ObjectAlreadyExistError("Ты уже написал комментарий")

    comment = Comment(item_id = data.item_id,rating = data.rating,
                      message = data.message,user_id = user_id)
    session.add(comment)
    session.flush()
    db_com_medias = []
    com_medias = []

    if media:
        for ind,file in enumerate(media):
            file_name = f"{data.item_id}.{user_id}.{ind}.{file.filename.split('.')[1]}"
            path = folder_path / file_name
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_com_medias.append(CommentMedia(url = str(file_name),media_type = file.content_type,comment_id = comment.id))
                com_medias.append(CommentMediaSchema(url=str(path),type = file.content_type))

        session.add_all(db_com_medias)
    return CommentSchema(id=comment.id, username=comment.users.name, message=comment.message,
                         rating=comment.rating,created_at=comment.created_at,
                         updated_at=comment.updated_at,media= com_medias)



def serv_delete_comment(item_id:int,user_id:int,session):
    comment = session.query(Comment).filter(Comment.user_id == user_id,Comment.item_id == item_id).first()
    if not comment:
        raise ObjectNotFoundError("Комментарий не найден")
    session.query(CommentMedia).filter(CommentMedia.comment_id == comment.id).delete()
    for file in folder_path.iterdir():
        if file.is_file() and f"{comment.id}." in file.name:
            file.unlink()
    session.delete(comment)
    return True

