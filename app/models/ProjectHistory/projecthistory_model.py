from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Projecthistory(Base):
    __tablename__ = 'projecthistories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project__name_ = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
