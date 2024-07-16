from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV2Interview(Base):
    __tablename__ = 'conversation_v2_interviews'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('admin_users.id'))
    category_id = Column(Integer, ForeignKey('conversation_v2_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('conversation_v2_categories_sub_categories.id'))
    current_question_id = Column(Integer, ForeignKey('conversation_v2_categories_sub_categories_questions.id'))
    scores = Column(Integer)
    max_scores = Column(Integer)
    percentage_score = Column(Integer)
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("AdminUser", back_populates="interviews")
    category = relationship("ConversationV2Category", back_populates="interviews")
    sub_category = relationship("ConversationV2CategoriesSubCategory", back_populates="interviews")
    messages = relationship("ConversationV2Message", back_populates="interview")
