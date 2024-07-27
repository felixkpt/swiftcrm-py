from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, Text, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class SocialMediaConversationCategoriesSubCategory(Base):
    __tablename__ = 'soc7e_media_conversation_categories_sub_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey('social_media_conversation_categories.id'))
    learn_instructions = Column(Text(None))
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
