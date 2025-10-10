from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Attribute(Base):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"),nullable=False)

    categories = relationship("Category", back_populates="attributes")
    attributes_value = relationship("AttributeValue", back_populates="attributes",cascade='delete')
