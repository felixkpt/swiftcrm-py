from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.models.base import Base

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class SysOpportunity(Base):
    __tablename__ = 'sys_opportunities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(String(255))
    updated_at = Column(String(255))
    source_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
