
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    info = Column(Text,nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)
    views_count = Column(Integer, default=0)

    categories = relationship("Category", back_populates="items")
    comments = relationship("Comment", back_populates="items")
    order_items = relationship("OrderItem", back_populates="items")
    basket_items = relationship("BasketItem", back_populates="items")
    favorites = relationship("FavoriteItem", back_populates="items")
    images = relationship("Image",back_populates="items")
    attributes_value = relationship("AttributeValue", back_populates="items")
    item_tags = relationship("ItemTag", back_populates="items")
    user_activities = relationship("UserActivity", back_populates="items")