from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV3WordConfidence(Base):
    __tablename__ = 'conversation_v3_word_confidences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('conversation_v3_messages.id'))
    word = Column(String(255))
    start_time_seconds = Column(Integer)
    end_time_seconds = Column(Integer)
    confidence = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
