
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,unique=True)

    item_tags = relationship("ItemTag", back_populates="tags",cascade='delete')
    user_tag_preferences = relationship("UserTagPreference", back_populates="tags",cascade='delete')