from app.database import db_session
from app.models.comment import Comment
from app.schemas.comment import CommentSchema, CommentUpdateSchema,CommentCreateSchema
from sqlalchemy.orm import joinedload

def serv_get_comments(item_id:int):
    with db_session() as session:
        comments = session.query(Comment).options(joinedload(Comment.users)).filter(Comment.item_id==item_id).all()
        return [CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                              rating = comment.rating,created_at=comment.created_at,
                              updated_at=comment.updated_at) for comment in comments]

def serv_patch_comment(item_id:int,user_id:int,new_data:CommentUpdateSchema):
    with db_session() as session:
        comment = session.query(Comment).filter(Comment.user_id ==user_id,Comment.item_id == item_id).first()
        if not comment:
            raise ValueError("Комментарий не найден")
        for key,val in new_data.model_dump(exclude_unset=True).items():
            setattr(comment,key,val)
        session.flush()
        return CommentSchema(id =comment.id,username=comment.users.name,message=comment.message,
                             rating = comment.rating,created_at=comment.created_at,
                             updated_at=comment.updated_at)

def serv_create_comment(data:CommentCreateSchema):
        with db_session() as session:
            is_available = session.query(Comment).filter(Comment.user_id == data.user_id,
                                                         Comment.item_id == data.item_id).first()
            if is_available:
                raise ValueError("Ты уже написал комментарий")

            comment = Comment(**data.model_dump())
            session.add(comment)
            session.flush()

            return CommentSchema(id=comment.id, username=comment.users.name, message=comment.message,
                                 rating=comment.rating,created_at=comment.created_at,
                                 updated_at=comment.updated_at)

def serv_delete_comment(item_id:int,user_id:int):
    with db_session() as session:
        comment = session.query(Comment).filter(Comment.user_id == user_id,Comment.item_id == item_id).first()
        if not comment:
            raise ValueError("Комментарий не найден")
        session.delete(comment)
        return True

