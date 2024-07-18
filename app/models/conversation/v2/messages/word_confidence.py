from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV2WordConfidence(Base):
    __tablename__ = 'conversation_v2_word_confidences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('conversation_v2_messages.id'), nullable=False)
    word = Column(String(255), nullable=False)
    start_time_seconds = Column(Integer)
    start_time_nanos = Column(Integer)
    end_time_seconds = Column(Integer)
    end_time_nanos = Column(Integer)
    confidence = Column(Float)

    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    message = relationship("ConversationV2Message", back_populates="word_confidences")
