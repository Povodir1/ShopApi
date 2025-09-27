
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    item_tags = relationship("ItemTag", back_populates="tags")
    user_tag_preferences = relationship("UserTagPreference", back_populates="tags")