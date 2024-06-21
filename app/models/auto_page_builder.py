from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey,func
from sqlalchemy.orm import relationship

class AutoPageBuilder(Base):
    __tablename__ = 'auto_page_builder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelName = Column(String(255), nullable=False)
    modelURI = Column(String(255), nullable=False)
    apiEndpoint = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    fields = relationship("AutoPageBuilderField", back_populates="page_builder", cascade="all, delete-orphan")
    action_labels = relationship("AutoPageBuilderActionLabel", back_populates="page_builder", cascade="all, delete-orphan")
    headers = relationship("AutoPageBuilderHeader", back_populates="page_builder", cascade="all, delete-orphan")
