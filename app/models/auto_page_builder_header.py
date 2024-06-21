# Import necessary modules from SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.models.base import Base


class AutoPageBuilderHeader(Base):
    __tablename__ = 'auto_page_builder_headers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_page_builder_id = Column(Integer, ForeignKey(
        'auto_page_builder.id'), nullable=False)
    key = Column(String(50), nullable=False)
    label = Column(String(255), nullable=False)
    isVisibleInList = Column(Integer, nullable=False, default=0)
    isVisibleInSingleView = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        server_default=func.now(), onupdate=func.now())

    page_builder = relationship("AutoPageBuilder", back_populates="headers")
