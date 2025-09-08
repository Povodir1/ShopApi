
from datetime import datetime
from sqlalchemy import Column, Integer, Text, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    is_main = Column(Boolean, default=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    items = relationship("Item", back_populates="images")