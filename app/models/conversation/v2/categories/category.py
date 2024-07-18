from sqlalchemy import Column, DateTime, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class ConversationV2Category(Base):
    __tablename__ = 'conversation_v2_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(Text(None))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    sub_category = relationship("ConversationV2CategoriesSubCategory", back_populates="category")
    messages = relationship("ConversationV2Message", back_populates="category")
    interviews = relationship("ConversationV2Interview", back_populates="category")
    questions = relationship("ConversationV2CategoriesSubCategoriesQuestion", back_populates="category")
