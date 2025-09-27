from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Text, Boolean,DateTime,Float
from sqlalchemy.orm import relationship
from app.models.base import Base
from datetime import datetime

class AttributeValue(Base):
    __tablename__ = "attributes_value"

    id = Column(Integer, primary_key=True)
    value = Column(Float)
    unit = Column(String)#enum
    attribute_id = Column(Integer,ForeignKey("attributes.id"))
    item_id = Column(Integer,ForeignKey("items.id"))

    attributes = relationship("Attribute", back_populates="attributes_value")
    items = relationship("Item", back_populates="attributes_value")