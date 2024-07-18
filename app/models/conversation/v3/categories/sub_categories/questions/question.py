from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV3CategoriesSubCategoriesQuestion(Base):
    __tablename__ = 'conversation_v3_categories_sub_categories_questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('conversation_v3_categories.id'))
    sub_category_id = Column(Integer)
    question = Column(Text(None))
    marks = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
