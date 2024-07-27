from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationMessage(Base):
    __tablename__ = 'social_media_conversation_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('social_media_conversation_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('soc7e_media_conversation_categories_sub_categories.id'))
    role = Column(String(255))
    mode = Column(String(255))
    content = Column(Text(None))
    interview_id = Column(Integer, ForeignKey('social_media_conversation_interviews.id'))
    question_id = Column(Integer, ForeignKey('soc4bversation_categories_sub_categories_questions.id'))
    question_scores = Column(Integer)
    audio_uri = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
