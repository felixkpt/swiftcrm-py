from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255), unique=True)
    email = Column(String(255), unique=True)
    alternate_number = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
