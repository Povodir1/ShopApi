


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey,Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class StatusList(enum.Enum):
    pending = "pending"
    paid = "paid"
    in_process = "in_process"

class PaymentMethods(enum.Enum):
    by_card = "by_card"
    by_cash = "by_cash"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    price = Column(DECIMAL(10, 2))
    status = Column(Enum(StatusList), default="pending")#enum
    payment_method = Column(Enum(PaymentMethods), nullable=False)#enum


    users = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders")
    addresses = relationship("Address",back_populates="orders")