from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    country = Column(String,nullable=False)
    city = Column(String,nullable=False)
    street = Column(String,nullable=False)
    home = Column(String,nullable=False)
    apartment_num = Column(String,nullable=False)

    orders = relationship("Order", back_populates="addresses",uselist=False)