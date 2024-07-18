from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class DashLead(Base):
    __tablename__ = 'dash_leads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey('conversation_v2_categories.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
