
from sqlalchemy import Column, Integer, DECIMAL,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    count = Column(Integer, default=1)
    item_price = Column(DECIMAL(10, 2))

    items = relationship("Item", back_populates="order_items")
    orders = relationship("Order", back_populates="order_items")