


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    price = Column(DECIMAL(10, 2))
    status = Column(String, default="pending")#enum
    address_id = Column(Integer, ForeignKey("addresses.id"))
    payment_method = Column(String, nullable=False)#enum


    users = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders")
    addresses = relationship("Address",back_populates="orsers")