import datetime
import os.path

from fastapi import UploadFile

from app.models import Comment, CommentMedia
from app.schemas.comment import CommentSchema, CommentUpdateSchema,CommentCreateSchema,CommentMediaSchema
from sqlalchemy.orm import joinedload
from app.exceptions import ObjectNotFoundError,ObjectAlreadyExistError

folder_path = os.path.join(os.path.abspath('.'), f"app/media/comments")

def serv_get_comments(item_id:int,session):
    comments = session.query(Comment).options(joinedload(Comment.users)).filter(Comment.item_id==item_id).all()
    comment_list = []
    for comment in comments:
        com_media = [CommentMediaSchema(url = med.url,type = med.media_type) for med in comment.comment_medias]

        com  = CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                              rating = comment.rating,media=com_media,created_at=comment.created_at,
                              updated_at=comment.updated_at)
        comment_list.append(com)
    return comment_list

async def serv_patch_comment(item_id:int,user_id:int,new_data:CommentUpdateSchema,media:list[UploadFile] |None,session):
    comment = session.query(Comment).filter(Comment.user_id ==user_id,Comment.item_id == item_id).first()
    if not comment:
        raise ObjectNotFoundError("Комментарий не найден")
    db_com_medias = []
    com_medias = []
    if media:
        [os.remove(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f"{comment.id}.{user_id}." in f]

        for ind, file in enumerate(media):
            path = os.path.join(folder_path, f"{comment.id}.{user_id}.{ind}.{file.filename.split('.')[1]}")
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_com_medias.append(CommentMedia(url=path, media_type=file.content_type, comment_id=comment.id))
                com_medias.append(CommentMediaSchema(url=path, type=file.content_type))

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
            path = os.path.join(folder_path,f"{comment.id}.{user_id}.{ind}.{file.filename.split('.')[1]}")
            with open(path, 'wb') as f:
                content = await file.read()
                f.write(content)
                db_com_medias.append(CommentMedia(url = path,media_type = file.content_type,comment_id = comment.id))
                com_medias.append(CommentMediaSchema(url=path,type = file.content_type))

        session.add_all(db_com_medias)
    return CommentSchema(id=comment.id, username=comment.users.name, message=comment.message,
                         rating=comment.rating,created_at=comment.created_at,
                         updated_at=comment.updated_at,media= com_medias)



def serv_delete_comment(item_id:int,user_id:int,session):
    comment = session.query(Comment).filter(Comment.user_id == user_id,Comment.item_id == item_id).first()
    if not comment:
        raise ObjectNotFoundError("Комментарий не найден")
    session.query(CommentMedia).filter(CommentMedia.comment_id == comment.id).delete()
    [os.remove(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f"{comment.id}.{user_id}." in f]
    session.delete(comment)
    return True

