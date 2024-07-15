from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationAppCategoriesSubCategoriesQuestion(Base):
    __tablename__ = 'conversation_app_categories_sub_categories_questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_app_category_id = Column(Integer, ForeignKey('conversation_app_categories.id'))
    conversation_app_categories_sub_category_id = Column(Integer, ForeignKey('conversation_app_categories_sub_categories.id'))
    question = Column(String(255))
    marks = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
