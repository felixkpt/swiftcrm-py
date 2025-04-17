from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Triage(Base):
    __tablename__ = '_triages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
