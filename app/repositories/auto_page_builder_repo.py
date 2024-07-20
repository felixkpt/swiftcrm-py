# app/repositories/auto_page_builder_repo.py
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from app.models.auto_page_builder import AutoPageBuilder
from app.models.auto_page_builder_field import AutoPageBuilderField
from app.models.auto_page_builder_action_label import AutoPageBuilderActionLabel
from app.models.auto_page_builder_header import AutoPageBuilderHeader


class AutoPageBuilderRepo:

    @staticmethod
    def get_page_by_id(db: Session, page_id: int):
        return db.query(AutoPageBuilder). \
            options(
                joinedload(AutoPageBuilder.fields),
                joinedload(AutoPageBuilder.action_labels),
                joinedload(AutoPageBuilder.headers)
        ). \
            filter(AutoPageBuilder.id == page_id). \
            first()

    @staticmethod
    def get_page_by_name(db: Session, name_singular: str):
        return db.query(AutoPageBuilder).filter(AutoPageBuilder.name_singular == name_singular).first()

    @staticmethod
    def get_page_by_table_name(db: Session, table_name_singular: str):
        return db.query(AutoPageBuilder).filter(AutoPageBuilder.table_name_singular == table_name_singular).first()

    @staticmethod
    def get_page_by_apiEndpoint(db: Session, apiEndpoint: str):
        return db.query(AutoPageBuilder).filter(AutoPageBuilder.apiEndpoint == apiEndpoint).first()

    @staticmethod
    def store_page(db: Session, auto_page_data):
        try:
            current_time = datetime.utcnow()
            new_page = AutoPageBuilder(
                name_singular=auto_page_data.name_singular,
                name_plural=auto_page_data.name_plural,
                modelURI=auto_page_data.modelURI,
                apiEndpoint=auto_page_data.apiEndpoint,
                table_name_singular=auto_page_data.table_name_singular,
                table_name_plural=auto_page_data.table_name_plural,
                class_name=auto_page_data.class_name,
                created_at=current_time,
                updated_at=current_time,
            )
            db.add(new_page)
            db.commit()

            for field in auto_page_data.fields:
                db_field = AutoPageBuilderField(
                    auto_page_builder_id=new_page.id,
                    name=field.name,
                    type=field.type,
                    label=field.label,
                    dataType=field.dataType,
                    defaultValue=field.defaultValue,
                    isRequired=field.isRequired,
                    isVisibleInList=field.isVisibleInList,
                    isVisibleInSingleView=field.isVisibleInSingleView,
                    isUnique=field.isUnique,
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

    @staticmethod
    def update_page(db: Session, page_id: int, auto_page_data):
        try:
            current_time = datetime.utcnow()

            db_page = db.query(AutoPageBuilder).filter(
                AutoPageBuilder.id == page_id).first()

            if db_page:
                db_page.name_singular = auto_page_data.name_singular
                db_page.name_plural = auto_page_data.name_plural
                db_page.modelURI = auto_page_data.modelURI
                db_page.apiEndpoint = auto_page_data.apiEndpoint
                db_page.table_name_singular = auto_page_data.table_name_singular
                db_page.table_name_plural = auto_page_data.table_name_plural
                db_page.class_name = auto_page_data.class_name
                db_page.updated_at = current_time

                # Clear existing fields, action labels, headers associated with this page_id
                db.query(AutoPageBuilderField).filter(
                    AutoPageBuilderField.auto_page_builder_id == page_id).delete()
                db.query(AutoPageBuilderActionLabel).filter(
                    AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
                db.query(AutoPageBuilderHeader).filter(
                    AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()

                # Store updated fields, action labels, headers
                for field in auto_page_data.fields:
                    db_field = AutoPageBuilderField(
                        auto_page_builder_id=page_id,
                        name=field.name,
                        type=field.type,
                        label=field.label,
                        dataType=field.dataType,
                        defaultValue=field.defaultValue,
                        isRequired=field.isRequired,
                        isVisibleInList=field.isVisibleInList,
                        isVisibleInSingleView=field.isVisibleInSingleView,
                        isUnique=field.isUnique,
                        dropdownSource=field.dropdownSource,
                        dropdownDependsOn=field.dropdownDependsOn,
                        desktopWidth=field.desktopWidth,
                        mobileWidth=field.mobileWidth,

                    )
                    db.add(db_field)

                for action_label in auto_page_data.actionLabels:
                    db_action_label = AutoPageBuilderActionLabel(
                        auto_page_builder_id=page_id,
                        key=action_label.key,
                        label=action_label.label,
                        actionType=action_label.actionType,
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

    @staticmethod
    def delete_page(db: Session, page_id: int):
        try:
            db_page = db.query(AutoPageBuilder).filter(
                AutoPageBuilder.id == page_id).first()
            if db_page:
                db.query(AutoPageBuilderField).filter(
                    AutoPageBuilderField.auto_page_builder_id == page_id).delete()
                db.query(AutoPageBuilderActionLabel).filter(
                    AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
                db.query(AutoPageBuilderHeader).filter(
                    AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()
                db.query(AutoPageBuilder).filter(
                    AutoPageBuilder.id == page_id).delete()
                db.commit()
                return {"message": "AutoPageBuilder configuration deleted successfully"}
            else:
                return {"message": "AutoPageBuilder configuration not found"}
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def get_pages(db: Session):
        data = db.query(AutoPageBuilder).all()
        results = {
            'data': data,
            'metadata': None,
        }
        return results
