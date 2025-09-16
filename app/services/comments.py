from app.database import db_session
from app.models.comment import Comment
from app.schemas.comment import CommentSchema
from sqlalchemy.orm import joinedload

def serv_get_comments(item_id:int):
    with db_session() as session:
        comments = session.query(Comment).options(joinedload(Comment.users)).filter(Comment.item_id==item_id).all()
        return [CommentSchema(username=comment.users.name,message=comment.message,rating = comment.rating,
                             created_at=comment.created_at,updated_at=comment.updated_at) for comment in comments]

def serv_patch_comment(item_id:int,user_id:int):
    pass