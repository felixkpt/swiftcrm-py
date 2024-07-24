from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AdminAutoBuildersModelBuilder(Base):
    __tablename__ = 'admin_auto_builders_model_builder_model_builders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(255))
    modelDisplayName = Column(String(255))
    name_singular = Column(String(255))
    name_plural = Column(String(255))
    modelURI = Column(String(255), unique=True)
    apiEndpoint = Column(String(255), unique=True)
    table_name_singular = Column(String(255), unique=True)
    table_name_plural = Column(String(255), unique=True)
    class_name = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    headers = relationship("AdminAutoBuildersModelBuilderModelHeader", back_populates="model_builder", cascade="all, delete-orphan")
    fields = relationship("AdminAutoBuildersModelBuilderModelField", back_populates="model_builder", cascade="all, delete-orphan")
    action_labels = relationship("AdminAutoBuildersModelBuilderActionLabel", back_populates="model_builder", cascade="all, delete-orphan")
