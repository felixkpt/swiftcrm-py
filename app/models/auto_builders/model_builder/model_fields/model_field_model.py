from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, JSON, String, func
from app.models.base import Base
from sqlalchemy.orm import relationship

class AutoBuildersModelBuilderModelField(Base):
    __tablename__ = 'auto_builders_model_builder_model_fields'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_builder_id = Column(Integer, ForeignKey('auto_builders_model_builders.id'))
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
    desktopWidth = Column(Integer)
    mobileWidth = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    status_id = Column(Integer, nullable=False, server_default='1')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    model_builder  = relationship("AutoBuildersModelBuilder", back_populates="fields")