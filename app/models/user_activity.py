
from sqlalchemy import Column, ForeignKey, Integer, DateTime,String
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime


class UserActivity(Base):
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    timestamp =  Column(DateTime, default=datetime.now)
    activity = Column(String)#enum


    users = relationship("User", back_populates="user_activities")
    items = relationship("Item", back_populates="user_activities")