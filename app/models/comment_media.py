from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey,Text
from sqlalchemy.orm import relationship
from app.models.base import Base

class CommentMedia(Base):
    __tablename__ = "comment_medias"

    id = Column(Integer, primary_key=True)
    comment_id = (Integer,ForeignKey("comments.id"))
    url = Column(Text, nullable=False)
    type = Column(String,nullable=False)#enum

    comments = relationship("Comment", back_populates="comment_medias")
