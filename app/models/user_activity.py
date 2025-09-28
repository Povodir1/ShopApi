
from sqlalchemy import Column, ForeignKey, Integer, DateTime,String,Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime
import enum

class ActivityType(enum.Enum):
    view = "view"
    add_to_basket = "add_to_basket"
    add_to_favorite = "add_to_favorite"

class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    timestamp =  Column(DateTime, default=datetime.now)
    activity = Column(Enum(ActivityType),nullable=False)#enum


    users = relationship("User", back_populates="user_activities")
    items = relationship("Item", back_populates="user_activities")