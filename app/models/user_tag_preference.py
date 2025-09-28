
from sqlalchemy import Column, Integer, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class UserTagPreference(Base):
    __tablename__ = "user_tag_preferences"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    score = Column(Integer)
    updated_at = Column(DateTime, default=datetime.now)

    tags = relationship("Tag",back_populates="user_tag_preferences")
    users = relationship("User", back_populates="user_tag_preferences")