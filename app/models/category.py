
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,unique=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))

    items = relationship("Item", back_populates="categories")
    attributes = relationship("Attribute", back_populates="categories")