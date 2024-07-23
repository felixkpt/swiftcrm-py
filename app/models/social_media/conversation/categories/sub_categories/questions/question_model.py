from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class Soc4e_iaConversationCategoriesSubCategoriesQuestion(Base):
    __tablename__ = 'soc4b_versation_categories_sub_categories_questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('social_media_conversation_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('social_media_conversation_categories_sub_categories.id'))
    question = Column(Text(None))
    marks = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
