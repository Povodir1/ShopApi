


from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey,Enum,CheckConstraint
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
    created_at = Column(DateTime,nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False,default=datetime.now, onupdate=datetime.now)
    status = Column(Enum(StatusList),nullable=False, default=StatusList.pending)
    payment_method = Column(Enum(PaymentMethods), nullable=False)

    __table_args__ = (
        CheckConstraint('updated_at >= created_at', name='valid_time'),)

    users = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="orders",cascade='delete')