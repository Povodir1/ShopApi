
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    info = Column(Text,nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)

    categories = relationship("Category", back_populates="items")
    comments = relationship("Comment", back_populates="items")
    order_items = relationship("OrderItem", back_populates="items")
    basket_items = relationship("BasketItem", back_populates="items")
    favorites = relationship("FavoriteItem", back_populates="items")
    images = relationship("Image",back_populates="items")