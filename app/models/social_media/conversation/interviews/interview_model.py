from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationInterview(Base):
    __tablename__ = 'social_media_conversation_interviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('social_media_conversation_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('soc7e_media_conversation_categories_sub_categories.id'))
    question_id = Column(Integer, ForeignKey('soc4bversation_categories_sub_categories_questions.id'))
    scores = Column(Integer)
    max_scores = Column(Integer)
    percentage_score = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
