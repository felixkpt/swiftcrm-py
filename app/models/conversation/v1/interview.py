# app/models/interview.py
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Interview(Base):
    __tablename__ = 'conversation_v1_interviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('conversation_v1_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('conversation_v1_sub_categories.id'))
    current_question_id = Column(Integer)
    scores = Column(Integer, nullable=True)
    max_scores = Column(Integer, nullable=True)
    percentage_score = Column(Integer, nullable=True)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="interviews")
    category = relationship("Category", back_populates="interviews")
    sub_category = relationship("SubCategory", back_populates="interviews")
    messages = relationship("Message", back_populates="interview")

