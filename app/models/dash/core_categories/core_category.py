from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class DashCoreCategory(Base):
    __tablename__ = 'dash_core_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('admin_users.id'))
    sub_category_id = Column(Integer, ForeignKey('conversation_v2_categories_sub_categories.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
