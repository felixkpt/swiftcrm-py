from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV2Message(Base):
    __tablename__ = 'conversation_v2_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('admin_users.id'))
    category_id = Column(Integer, ForeignKey('conversation_v2_categories.id'))
    sub_category_id = Column(Integer, ForeignKey('conversation_v2_categories_sub_categories.id'))
    role = Column(String(255))
    mode = Column(String(255))
    interview_id = Column(Integer, ForeignKey('conversation_v2_interviews.id'))
    question_id = Column(Integer, ForeignKey('conversation_v2_categories_sub_categories_questions.id'))
    question_scores = Column(Integer)
    content = Column(Text(None))
    audio_uri = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("AdminUser", back_populates="messages")
    category = relationship("ConversationV2Category", back_populates="messages")
    sub_category = relationship("ConversationV2CategoriesSubCategory", back_populates="messages")
    interview = relationship("ConversationV2Interview", back_populates="messages")
    word_confidences = relationship("ConversationV2WordConfidence", back_populates="message")
