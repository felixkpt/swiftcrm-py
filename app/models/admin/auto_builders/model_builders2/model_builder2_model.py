from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AdminAutoBuildersModelBuilders2ModelBuilder2(Base):
    __tablename__ = 'adm7dauto_builders_model_builders2_model_builder2s'
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
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
