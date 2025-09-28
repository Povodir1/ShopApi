from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class ItemTag(Base):
    __tablename__ = "item_tags"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer,ForeignKey("tags.id"))
    item_id = Column(Integer,ForeignKey("items.id"))

    items = relationship("Item", back_populates="item_tags")
    tags = relationship("Tag", back_populates="item_tags")