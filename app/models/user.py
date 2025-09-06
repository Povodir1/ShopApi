
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text
from sqlalchemy.orm import relationship
from base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    money = Column(DECIMAL(10, 2), default=0)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.now())

    comments = relationship("Comment", back_populates="users")
    orders = relationship("Order", back_populates="users")
    favourites = relationship("FavouriteItem", back_populates="users")
    basket_items = relationship("BasketItem", back_populates="users")