from sqlalchemy import Column, Integer, ForeignKey,Boolean,String
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum




class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    resource = Column(String, nullable=False)
    action = Column(String, nullable=False)

    roles = relationship("Role",back_populates="permissions")
