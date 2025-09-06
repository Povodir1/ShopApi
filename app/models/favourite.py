
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from base import Base


class FavoriteItem(Base):
    __tablename__ = "favorite_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    users = relationship("User", back_populates="favorites")
    items = relationship("Item", back_populates="favorites")