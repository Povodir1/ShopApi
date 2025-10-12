from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum


class CommentMedia(Base):
    __tablename__ = "comment_medias"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer,ForeignKey("comments.id"),nullable=False)
    url = Column(Text, nullable=False)
    media_type = Column(String,nullable=False)

    comments = relationship("Comment", back_populates="comment_medias")
