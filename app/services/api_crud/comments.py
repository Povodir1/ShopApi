from app.database import db_session
from app.models import Comment, CommentMedia
from app.schemas.comment import CommentSchema, CommentUpdateSchema,CommentCreateSchema,CommentMediaSchema
from sqlalchemy.orm import joinedload

def serv_get_comments(item_id:int):
    with db_session() as session:
        comments = session.query(Comment).options(joinedload(Comment.users)).filter(Comment.item_id==item_id).all()
        comment_list = []
        for comment in comments:
            com_media = [CommentMediaSchema(url = med.url,type = med.type) for med in comment.comment_medias]

            com  = CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                                  rating = comment.rating,media=com_media,created_at=comment.created_at,
                                  updated_at=comment.updated_at)
            comment_list.append(com)
        return comment_list

def serv_patch_comment(item_id:int,user_id:int,new_data:CommentUpdateSchema):
    with db_session() as session:
        comment = session.query(Comment).filter(Comment.user_id ==user_id,Comment.item_id == item_id).first()
        if not comment:
            raise ValueError("Комментарий не найден")
        print(new_data.media)
        if new_data.media:
            com_medias = [CommentMedia(url=med.url, type=med.type,comment_id = comment.id) for med in new_data.media]
            session.query(CommentMedia).filter(CommentMedia.comment_id == comment.id).delete()
            session.add_all(com_medias)
            new_data.media = None


        for key,val in new_data.model_dump(exclude_none=True).items():
            setattr(comment,key,val)
        session.flush()
        medias = [CommentMediaSchema(url=med.url, type=med.type) for med in comment.comment_medias]
        return CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                             rating = comment.rating,created_at=comment.created_at,
                             updated_at=comment.updated_at,media=medias)


def serv_create_comment(data:CommentCreateSchema,user_id:int):
        with db_session() as session:
            is_available = session.query(Comment).filter(Comment.user_id == user_id,
                                                         Comment.item_id == data.item_id).first()
            if is_available:
                raise ValueError("Ты уже написал комментарий")

            comment = Comment(item_id = data.item_id,rating = data.rating,
                              message = data.message,user_id = user_id)
            session.add(comment)
            session.flush()
            com_medias = [CommentMedia(url = med.url,type = med.type,comment_id = comment.id) for med in data.media]
            session.add_all(com_medias)
            return CommentSchema(id=comment.id, username=comment.users.name, message=comment.message,
                                 rating=comment.rating,created_at=comment.created_at,
                                 updated_at=comment.updated_at,media= data.media)

def serv_delete_comment(item_id:int,user_id:int):
    with db_session() as session:
        comment = session.query(Comment).filter(Comment.user_id == user_id,Comment.item_id == item_id).first()
        if not comment:
            raise ValueError("Комментарий не найден")
        session.query(CommentMedia).filter(CommentMedia.comment_id == comment.id).delete()
        session.delete(comment)
        return True

