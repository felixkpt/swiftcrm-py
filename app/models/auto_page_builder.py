# Assuming this is app/models/auto_page_builder.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship, joinedload
from app.models.base import Base
# CRUD Operations in the same file
from sqlalchemy.orm import Session
from app.models.auto_page_builder_field import AutoPageBuilderField
from app.models.auto_page_builder_action_label import AutoPageBuilderActionLabel
from app.models.auto_page_builder_header import AutoPageBuilderHeader

class AutoPageBuilder(Base):
    __tablename__ = 'auto_page_builder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelName = Column(String(255), nullable=False)
    modelURI = Column(String(255), nullable=False)
    apiEndpoint = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    fields = relationship("AutoPageBuilderField", back_populates="page_builder", cascade="all, delete-orphan")
    action_labels = relationship("AutoPageBuilderActionLabel", back_populates="page_builder", cascade="all, delete-orphan")
    headers = relationship("AutoPageBuilderHeader", back_populates="page_builder", cascade="all, delete-orphan")

def get_page_by_id(db: Session, page_id: int):
    return db.query(AutoPageBuilder). \
        options(
            joinedload(AutoPageBuilder.fields),
            joinedload(AutoPageBuilder.action_labels),
            joinedload(AutoPageBuilder.headers)
        ). \
        filter(AutoPageBuilder.id == page_id). \
        first()

def get_page_by_name(db: Session, modelName: str):
    return db.query(AutoPageBuilder).filter(AutoPageBuilder.modelName == modelName).first()

def store_page(db: Session, auto_page_data):
    try:
        current_time = datetime.utcnow()
        new_page = AutoPageBuilder(
            modelName=auto_page_data.modelName,
            modelURI=auto_page_data.modelURI,
            apiEndpoint=auto_page_data.apiEndpoint,
            created_at=current_time,
            updated_at=current_time
        )
        db.add(new_page)
        db.commit()

        for field in auto_page_data.fields:
            db_field = AutoPageBuilderField(
                auto_page_builder_id=new_page.id,
                name=field.name,
                type=field.type,
                label=field.label,
                isRequired=field.isRequired,
                dataType=field.dataType,
                defaultValue=field.defaultValue,
                dropdownSource=field.dropdownSource,
                dropdownDependsOn=field.dropdownDependsOn
            )
            db.add(db_field)

        for action_label in auto_page_data.actionLabels:
            db_action_label = AutoPageBuilderActionLabel(
                auto_page_builder_id=new_page.id,
                key=action_label.key,
                label=action_label.label,
                actionType=action_label.actionType,
                show=action_label.show
            )
            db.add(db_action_label)

        for header in auto_page_data.headers:
            db_header = AutoPageBuilderHeader(
                auto_page_builder_id=new_page.id,
                key=header.key,
                label=header.label,
                isVisibleInList=header.isVisibleInList,
                isVisibleInSingleView=header.isVisibleInSingleView
            )
            db.add(db_header)

        db.commit()
        return {"message": "AutoPageBuilder configuration stored successfully"}

    except Exception as e:
        db.rollback()
        raise e

def update_page(db: Session, page_id: int, auto_page_data):
    try:
        current_time = datetime.utcnow()
        db_page = db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).first()
        if db_page:
            db_page.modelName = auto_page_data.modelName
            db_page.modelURI = auto_page_data.modelURI
            db_page.apiEndpoint = auto_page_data.apiEndpoint
            db_page.updated_at = current_time

            # Clear existing fields, action labels, headers associated with this page_id
            db.query(AutoPageBuilderField).filter(AutoPageBuilderField.auto_page_builder_id == page_id).delete()
            db.query(AutoPageBuilderActionLabel).filter(AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
            db.query(AutoPageBuilderHeader).filter(AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()

            # Store updated fields, action labels, headers
            for field in auto_page_data.fields:
                db_field = AutoPageBuilderField(
                    auto_page_builder_id=page_id,
                    name=field.name,
                    type=field.type,
                    label=field.label,
                    isRequired=field.isRequired,
                    dataType=field.dataType,
                    defaultValue=field.defaultValue,
                    dropdownSource=field.dropdownSource,
                    dropdownDependsOn=field.dropdownDependsOn
                )
                db.add(db_field)

            for action_label in auto_page_data.actionLabels:
                db_action_label = AutoPageBuilderActionLabel(
                    auto_page_builder_id=page_id,
                    key=action_label.key,
                    label=action_label.label,
                    actionType=action_label.actionType,
                    show=action_label.show
                )
                db.add(db_action_label)

            for header in auto_page_data.headers:
                db_header = AutoPageBuilderHeader(
                    auto_page_builder_id=page_id,
                    key=header.key,
                    label=header.label,
                    isVisibleInList=header.isVisibleInList,
                    isVisibleInSingleView=header.isVisibleInSingleView
                )
                db.add(db_header)

            db.commit()
            return {"message": "AutoPageBuilder configuration updated successfully"}
        else:
            return {"message": "AutoPageBuilder configuration not found"}

    except Exception as e:
        db.rollback()
        raise e

def delete_page(db: Session, page_id: int):
    try:
        db_page = db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).first()
        if db_page:
            db.query(AutoPageBuilderField).filter(AutoPageBuilderField.auto_page_builder_id == page_id).delete()
            db.query(AutoPageBuilderActionLabel).filter(AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
            db.query(AutoPageBuilderHeader).filter(AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()
            db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).delete()
            db.commit()
            return {"message": "AutoPageBuilder configuration deleted successfully"}
        else:
            return {"message": "AutoPageBuilder configuration not found"}
    except Exception as e:
        db.rollback()
        raise e

def get_pages(db: Session):
    return db.query(AutoPageBuilder).all()
