from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationCategoriesSubCategoriesQuestion(Base):
    __tablename__ = 'wthhdia_conversation_categories_sub_categories_questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('social_media_conversation_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('social_media_conversation_categories_sub_categories.id'))
    question = Column(String(255))
    marks = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
