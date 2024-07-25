from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AutoBuildersModelBuilderActionLabel(Base):
    __tablename__ = 'auto_builders_model_builder_action_labels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_builder_id = Column(Integer)
    key = Column(String(255))
    label = Column(String(255))
    actionType = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
