from sqlalchemy import Column, Integer, String, DateTime, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'conversation_v1_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    
    sub_category = relationship("SubCategory", back_populates="category")
    messages = relationship("Message", back_populates="category")
    interviews = relationship("Interview", back_populates="category")
    questions = relationship("Question", back_populates="category")

