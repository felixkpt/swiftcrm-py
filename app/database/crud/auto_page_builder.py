from sqlalchemy.orm import Session
from app.models.auto_page_builder import AutoPageBuilder
from app.models.auto_page_builder_field import AutoPageBuilderField
from app.models.auto_page_builder_action_label import AutoPageBuilderActionLabel
from app.models.auto_page_builder_header import AutoPageBuilderHeader

def get_page_by_id(db: Session, page_id: int):
    return db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).first()

def get_page_by_name(db: Session, modelName: str):
    return db.query(AutoPageBuilder).filter(AutoPageBuilder.modelName == modelName).first()

def store_page(db: Session, auto_page_data):
    
    try:
        # Create AutoPageBuilder instance
        new_page = AutoPageBuilder(
            modelName=auto_page_data.modelName,
            modelUri=auto_page_data.modelURI,
            apiEndpoint=auto_page_data.apiEndpoint
        )
        print('new_page',new_page)

        # db.add(new_page)
        # db.commit()

        # Store fields
        # for field in auto_page_data.fields:
        #     db_field = AutoPageBuilderField(
        #         auto_page_builder_id=new_page.id,
        #         name=field.name,
        #         type=field.type,
        #         label=field.label,
        #         isRequired=field.isRequired,
        #         dataType=field.dataType,
        #         defaultValue=field.defaultValue,
        #         dropdownSource=field.dropdownSource,
        #         dropdownDependsOn=field.dropdownDependsOn
        #     )
        #     db.add(db_field)

        # # Store action labels
        # for action_label in auto_page_data.actionLabels:
        #     db_action_label = AutoPageBuilderActionLabel(
        #         auto_page_builder_id=new_page.id,
        #         key=action_label.key,
        #         label=action_label.label,
        #         actionType=action_label.actionType,
        #         show=action_label.show
        #     )
        #     db.add(db_action_label)

        # # Store headers
        # for header in auto_page_data.headers:
        #     db_header = AutoPageBuilderHeader(
        #         auto_page_builder_id=new_page.id,
        #         key=header.key,
        #         label=header.label,
        #         isVisibleInList=header.isVisibleInList,
        #         isVisibleInSingleView=header.isVisibleInSingleView
        #     )
        #     db.add(db_header)

        db.commit()
        return {"message": "AutoPageBuilder configuration stored successfully"}

    except Exception as e:
        db.rollback()
        raise e

def update_page(db: Session, page_id: int, auto_page_data):
    try:
        # Update AutoPageBuilder instance
        db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).update({
            AutoPageBuilder.modelName: auto_page_data.modelName,
            AutoPageBuilder.modelUri: auto_page_data.modelURI,
            AutoPageBuilder.apiEndpoint: auto_page_data.apiEndpoint
        })

        # Clear existing fields, action labels, headers associated with this page_id
        db.query(AutoPageBuilderField).filter(AutoPageBuilderField.auto_page_builder_id == page_id).delete()
        db.query(AutoPageBuilderActionLabel).filter(AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
        db.query(AutoPageBuilderHeader).filter(AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()

        # Store updated fields
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

        # Store updated action labels
        for action_label in auto_page_data.actionLabels:
            db_action_label = AutoPageBuilderActionLabel(
                auto_page_builder_id=page_id,
                key=action_label.key,
                label=action_label.label,
                actionType=action_label.actionType,
                show=action_label.show
            )
            db.add(db_action_label)

        # Store updated headers
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

    except Exception as e:
        db.rollback()
        raise e

def delete_page(db: Session, page_id: int):
    try:
        # Delete AutoPageBuilder instance
        db.query(AutoPageBuilder).filter(AutoPageBuilder.id == page_id).delete()

        # Delete associated fields, action labels, headers
        db.query(AutoPageBuilderField).filter(AutoPageBuilderField.auto_page_builder_id == page_id).delete()
        db.query(AutoPageBuilderActionLabel).filter(AutoPageBuilderActionLabel.auto_page_builder_id == page_id).delete()
        db.query(AutoPageBuilderHeader).filter(AutoPageBuilderHeader.auto_page_builder_id == page_id).delete()

        db.commit()
        return {"message": "AutoPageBuilder configuration deleted successfully"}

    except Exception as e:
        db.rollback()
        raise e

def get_pages(db: Session):
    return db.query(AutoPageBuilder).all()
