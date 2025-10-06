from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class AttributeValue(Base):
    __tablename__ = "attributes_value"

    id = Column(Integer, primary_key=True)
    value = Column(String)
    unit = Column(String)
    attribute_id = Column(Integer,ForeignKey("attributes.id"))
    item_id = Column(Integer,ForeignKey("items.id"))

    attributes = relationship("Attribute", back_populates="attributes_value")
    items = relationship("Item", back_populates="attributes_value")

