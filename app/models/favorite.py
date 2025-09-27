
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime


class FavoriteItem(Base):
    __tablename__ = "favorite_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    added_at =  Column(DateTime, default=datetime.now)

    users = relationship("User", back_populates="favorites")
    items = relationship("Item", back_populates="favorites")