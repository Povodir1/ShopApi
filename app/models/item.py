
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean,DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    info = Column(Text,nullable=False)
    stock = Column(Integer, nullable=False,default=0)
    category_id = Column(Integer, ForeignKey("categories.id"),nullable=False)
    created_at = Column(DateTime,nullable=False, default=datetime.now)
    updated_at = Column(DateTime,nullable=False, default=datetime.now)
    is_active = Column(Boolean,nullable=False, default=True)
    views_count = Column(Integer,nullable=False, default=0)

    __table_args__ = (
        CheckConstraint('price >= 0 AND views_count >= 0 AND stock >= 0', name='positive_int'),
        CheckConstraint('updated_at >= created_at', name  = 'valid_time'))

    categories = relationship("Category", back_populates="items")
    comments = relationship("Comment", back_populates="items")
    order_items = relationship("OrderItem", back_populates="items")
    basket_items = relationship("BasketItem", back_populates="items")
    favorites = relationship("FavoriteItem", back_populates="items")
    images = relationship("Image",back_populates="items")
    attributes_value = relationship("AttributeValue", back_populates="items")
    item_tags = relationship("ItemTag", back_populates="items")