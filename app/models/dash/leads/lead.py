from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class DashLead(Base):
    __tablename__ = 'dash_leads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dash_leads_categories_lead_category_id = Column(Integer, ForeignKey('dash_leads_categories_lead_categories.id'))
    comments = Column(Text(None))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
