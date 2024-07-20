from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV3Interview(Base):
    __tablename__ = 'conversation_v3_interviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    category_id = Column(Integer, ForeignKey('conversation_v3_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('conversation_v3_categories_sub_categories.id'))
    question_id = Column(Integer, ForeignKey('conversation_v3_categories_sub_categories_questions.id'))
    scores = Column(Integer)
    max_scores = Column(Integer)
    percentage_score = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("AdminUser", back_populates="interviews")
    category = relationship("ConversationV3Category", back_populates="interviews")
    sub_category = relationship("ConversationV3CategoriesSubCategory", back_populates="interviews")
    messages = relationship("ConversationV3Message", back_populates="interview")
