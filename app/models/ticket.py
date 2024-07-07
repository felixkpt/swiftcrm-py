from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.models.base import Base

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(String(255))
    updated_at = Column(String(255))
    source_id = Column(Integer)
    comment = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
