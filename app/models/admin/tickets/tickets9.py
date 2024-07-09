from sqlalchemy import Column, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship


class Tickets9(Base):
    __tablename__ = 'admin_tickets_tickets9s'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
