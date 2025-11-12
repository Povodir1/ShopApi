
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Text, Boolean, Enum,CheckConstraint,ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

from app.core.enums import LanguageList,CurrencyType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,default='nameless')
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    money = Column(DECIMAL(10, 2,),nullable=False, default=0)
    role_id = Column(Integer,ForeignKey("roles.id"))
    created_at = Column(DateTime,nullable=False, default=datetime.now)
    last_login = Column(DateTime,nullable=False, default=datetime.now)
    is_banned = Column(Boolean,nullable=False,default=False)
    language = Column(Enum(LanguageList),nullable=False,default=LanguageList.ru)
    currency = Column(Enum(CurrencyType),nullable=False,default=CurrencyType.USD)

    __table_args__ = (
        CheckConstraint('money >= 0', name='positive_int'),
        CheckConstraint('last_login >= created_at', name='valid_time'),
        CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='valid_email_format')
    )

    comments = relationship("Comment", back_populates="users",cascade='delete')
    orders = relationship("Order", back_populates="users")
    favorites = relationship("FavoriteItem", back_populates="users",cascade='delete')
    basket_items = relationship("BasketItem", back_populates="users",cascade='delete')
    user_tag_preferences = relationship("UserTagPreference", back_populates="users",cascade='delete')
    roles = relationship("Role",back_populates="users")

