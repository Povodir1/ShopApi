
from sqlalchemy import Column, Integer, ForeignKey,DateTime,CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class UserTagPreference(Base):
    __tablename__ = "user_tag_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"),nullable=False)
    score = Column(Integer,nullable=False,default=1)
    updated_at = Column(DateTime,nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint('score >= 1', name='positive_int'),)
    tags = relationship("Tag",back_populates="user_tag_preferences")
    users = relationship("User", back_populates="user_tag_preferences")