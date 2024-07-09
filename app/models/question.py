from sqlalchemy import Column, Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"))
    question = Column(Text)
    marks = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="questions")
    sub_category = relationship("SubCategory", back_populates="questions")
    