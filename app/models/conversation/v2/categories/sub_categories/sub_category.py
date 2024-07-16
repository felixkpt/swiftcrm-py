from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV2CategoriesSubCategory(Base):
    __tablename__ = 'conversation_v2_categories_sub_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey('conversation_v2_categories.id'))
    learn_instructions = Column(Text(None))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("ConversationV2Category", back_populates="sub_category")
    questions = relationship("ConversationV2CategoriesSubCategoriesQuestion", back_populates="sub_category")
    messages = relationship("ConversationV2Message", back_populates="sub_category")
    interviews = relationship("ConversationV2Interview", back_populates="sub_category")
