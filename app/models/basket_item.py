from sqlalchemy import Column, Integer, ForeignKey, DateTime,CheckConstraint
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.base import Base

class BasketItem(Base):
    __tablename__ = "basket_items"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"),nullable=False)
    added_at =  Column(DateTime,nullable=False, default=datetime.now)
    count = Column(Integer,nullable=False, default=1)

    __table_args__ = (
        CheckConstraint('count >= 1', name='positive_int'),)

    users = relationship("User", back_populates="basket_items")
    items = relationship("Item", back_populates="basket_items")





