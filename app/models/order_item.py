
from sqlalchemy import Column, Integer, DECIMAL,ForeignKey,CheckConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"),nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"),nullable=False)
    count = Column(Integer,nullable=False, default=1)
    item_price = Column(DECIMAL(10, 2),nullable=False)

    __table_args__ = (
        CheckConstraint('count >= 0', name='positive_int'),)

    items = relationship("Item", back_populates="order_items")
    orders = relationship("Order", back_populates="order_items")