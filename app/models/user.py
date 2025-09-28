
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class LanguageList(enum.Enum):
    ru = "russian"
    en = "english"

class CurrencyType(enum.Enum):
    byn = "BYN"
    usd = "USD"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    money = Column(DECIMAL(10, 2), default=0)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime, default=datetime.now)
    is_banned = Column(Boolean,default=False)
    language = Column(String,default="ru") #enum
    currency = Column(String,default="usd") #enum

    comments = relationship("Comment", back_populates="users")
    orders = relationship("Order", back_populates="users")
    favorites = relationship("FavoriteItem", back_populates="users")
    basket_items = relationship("BasketItem", back_populates="users")
    user_tag_preferences = relationship("UserTagPreference", back_populates="users")
    user_activities = relationship("UserActivity", back_populates="users")