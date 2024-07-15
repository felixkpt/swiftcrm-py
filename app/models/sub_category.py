from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class SubCategory(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String(255))
    slug = Column(String(255))
    learn_instructions = Column(Text)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="sub_category")
    questions = relationship("Question", back_populates="sub_category")
    messages = relationship("Message", back_populates="sub_category")
    interviews = relationship("Interview", back_populates="sub_category")
