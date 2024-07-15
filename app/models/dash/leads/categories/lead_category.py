from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class DashLeadsCategoriesleadCategory(Base):
    __tablename__ = 'dash_leads_categories_lead_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    description = Column(Text(None))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
