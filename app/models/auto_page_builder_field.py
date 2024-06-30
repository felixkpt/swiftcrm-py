from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, func, JSON
from sqlalchemy.orm import relationship


class AutoPageBuilderField(Base):
    __tablename__ = 'auto_page_builder_fields'

    id = Column(Integer, primary_key=True, autoincrement=True)
    auto_page_builder_id = Column(Integer, ForeignKey(
        'auto_page_builder.id'), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    label = Column(String(255), nullable=False)
    dataType = Column(String(50))
    defaultValue = Column(Text)
    isRequired = Column(Integer, nullable=False, default=0)
    isVisibleInList = Column(Integer, nullable=False, default=0)
    isVisibleInSingleView = Column(Integer, nullable=False, default=0)
    isUnique = Column(Integer, nullable=False, default=0)
    dropdownSource = Column(String(255), nullable=True)
    dropdownDependsOn = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        server_default=func.now(), onupdate=func.now())

    page_builder = relationship("AutoPageBuilder", back_populates="fields")

