from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AdminAutoBuildersModelBuilderActionLabel(Base):
    __tablename__ = 'admin_auto_builders_model_builder_action_labels'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_builder_id = Column(Integer, ForeignKey('admin_auto_builders_model_builder_model_builders.id'))
    key = Column(String(255))
    label = Column(String(255))
    actionType = Column(String(255))
    show = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    model_builder = relationship("AdminAutoBuildersModelBuilder", back_populates="action_labels")
