
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    items = relationship("Item", back_populates="categories")
