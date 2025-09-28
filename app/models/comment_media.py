from sqlalchemy import Column, Integer, String, ForeignKey,Text,Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class MediaType(enum.Enum):
    video = "video"
    image = "image"


class CommentMedia(Base):
    __tablename__ = "comment_medias"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer,ForeignKey("comments.id"))
    url = Column(Text, nullable=False)
    type = Column(Enum(MediaType),nullable=False)#enum

    comments = relationship("Comment", back_populates="comment_medias")
