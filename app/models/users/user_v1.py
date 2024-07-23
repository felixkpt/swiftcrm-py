from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users_v1'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    refresh_tokens = relationship("RefreshToken", back_populates="user")

