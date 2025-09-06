
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Text, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    is_main = Column(Boolean, default=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    items = relationship("Item", back_populates="images")