from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AdminAutoBuildersModelBuilderModelField(Base):
    __tablename__ = 'admin_auto_builders_model_builder_model_fields'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_builder_id = Column(Integer, ForeignKey('admin_auto_builders_model_builder_model_builders.id'))
    name = Column(String(255))
    type = Column(String(255))
    label = Column(String(255))
    dataType = Column(String(255))
    defaultValue = Column(String(255))
    isVisibleInList = Column(Integer)
    isVisibleInSingleView = Column(Integer)
    isRequired = Column(Integer)
    isUnique = Column(Integer)
    dropdownSource = Column(String(255))
    dropdownDependsOn = Column(JSON(None))
    desktopWidth = Column(String(255))
    mobileWidth = Column(String(255))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    model_builder  = relationship("AdminAutoBuildersModelBuilder", back_populates="fields")
