from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean,DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    categories = relationship("Category", back_populates="attributes")
    attributes_value = relationship("AttributeValue", back_populates="attributes")
