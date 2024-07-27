from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationMessagesWordConfidence(Base):
    __tablename__ = 'soccc_media_conversation_messages_word_confidences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('social_media_conversation_messages.id'))
    word = Column(String(255))
    start_time_seconds = Column(Integer)
    start_time_nanos = Column(String(255))
    end_time_seconds = Column(Integer)
    end_time_nanos = Column(Integer)
    confidence = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
