from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AutoBuildersModelBuilder(Base):
    __tablename__ = 'auto_builders_model_builders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255), unique=True)
    modelDisplayName = Column(String(255))
    nameSingular = Column(String(255))
    namePlural = Column(String(255))
    modelURI = Column(String(255), unique=True)
    apiEndpoint = Column(String(255), unique=True)
    tableNameSingular = Column(String(255), unique=True)
    tableNamePlural = Column(String(255), unique=True)
    className = Column(String(255))
    createFrontendViews = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    headers = relationship("AutoBuildersModelBuilderModelHeader", back_populates="model_builder", cascade="all, delete-orphan")
    fields = relationship("AutoBuildersModelBuilderModelField", back_populates="model_builder", cascade="all, delete-orphan")
    action_labels = relationship("AutoBuildersModelBuilderActionLabel", back_populates="model_builder", cascade="all, delete-orphan")
