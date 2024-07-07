from sqlalchemy import Column, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship


class Justcat(Base):
    __tablename__ = 'justcats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    description = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
