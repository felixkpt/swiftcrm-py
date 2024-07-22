from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationCategoriesSubCategory(Base):
    __tablename__ = 'social_media_conversation_categories_sub_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_category_id = Column(Integer)
    name = Column(String(255))
    learn_instructions = Column(Text(None))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
