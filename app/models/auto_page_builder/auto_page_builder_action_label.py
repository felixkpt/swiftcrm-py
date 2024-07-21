from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship


class AutoPageBuilderActionLabel(Base):
    __tablename__ = 'auto_page_builder_action_labels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_page_builder_id = Column(Integer, ForeignKey(
        'auto_page_builder.id'), nullable=False)
    key = Column(String(50), nullable=False)
    label = Column(String(255), nullable=False)
    actionType = Column(String(50), nullable=False)
    show = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        server_default=func.now(), onupdate=func.now())

    page_builder = relationship(
        "AutoPageBuilder", back_populates="action_labels")
