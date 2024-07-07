# app/models/message.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    sub_category_id = Column(Integer, ForeignKey('sub_categories.id'))
    role = Column(Enum('user', 'assistant'))
    mode = Column(Enum('training', 'interview'))
    interview_id = Column(Integer, ForeignKey('interviews.id', ondelete='CASCADE'), nullable=True)
    question_id = Column(Integer, nullable=True)
    question_scores = Column(Integer, nullable=True)
    content = Column(Text)
    audio_uri = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="messages")
    category = relationship("Category", back_populates="messages")
    sub_category = relationship("SubCategory", back_populates="messages")
    interview = relationship("Interview", back_populates="messages")
