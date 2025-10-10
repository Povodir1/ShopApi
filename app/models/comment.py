from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime,CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

from datetime import datetime



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"),nullable=False)
    message = Column(Text)
    rating = Column(Integer,nullable=False)
    created_at = Column(DateTime,nullable=False, default=datetime.now)
    updated_at = Column(DateTime,nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5', name='positive_int'),
        CheckConstraint('updated_at >= created_at', name  = 'valid_time'))

    users = relationship("User", back_populates="comments")
    items = relationship("Item", back_populates="comments")
    comment_medias = relationship("CommentMedia", back_populates="comments",cascade='delete')