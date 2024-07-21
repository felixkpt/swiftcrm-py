from datetime import datetime
from sqlalchemy.orm import joinedload
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.auto_builders.model_builder.model_builder import AdminAutoBuildersModelBuilder as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.repositories.admin.auto_builders.model_builder.model_fields.model_field_repo import ModelFieldRepo
from app.repositories.admin.auto_builders.model_builder.model_headers.model_header_repo import ModelHeaderRepo
from app.repositories.admin.auto_builders.model_builder.action_labels.action_label_repo import ActionLabelRepo


class ModelBuilderRepo(BaseRepo):

    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['name_singular', 'name_plural', 'modelURI',
                         'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        query = apply_common_filters(
            db.query(Model), Model, search_fields, query_params)
        metadata = set_metadata(query, query_params)
        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])
        return {"records": query.all(), "metadata": metadata}

    def repo_specific_filters(self, query, Model, query_params):
        for field in ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']:
            value = query_params.get(field, '').strip()
            if value:
                query = query.filter(getattr(Model, field).ilike(f'%{value}%'))
        return query

    async def create(self, db: Session, model_request):
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(
            db, Model, model_request, unique_fields)
        current_time = datetime.now()
        new_model = Model(
            created_at=current_time,
            updated_at=current_time,
            **{field: getattr(model_request, field) for field in required_fields}
        )
        db.add(new_model)
        try:
            db.commit()
            db.refresh(new_model)
            # Store fields, headers, and action labels using their respective repositories
            created_fields = []
            for field in model_request.fields:
                field.model_builder_id = new_model.id
                created_field = await ModelFieldRepo().create(db, field)
                created_fields.append(created_field)
            
            created_headers = []
            for header in model_request.headers:
                header.model_builder_id = new_model.id
                created_header = await ModelHeaderRepo().create(db, header)
                created_headers.append(created_header)
            
            created_action_labels = []
            for action_label in model_request.actionLabels:
                action_label.model_builder_id = new_model.id
                created_action_label = await ActionLabelRepo().create(db, action_label)
                created_action_labels.append(created_action_label)

            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        
        # Convert the model to a dictionary
        model_data = {column.name: getattr(new_model, column.name) for column in new_model.__table__.columns}
        # Combine and return the main model with its related objects
        combined_result = {
            **model_data,
            "fields": created_fields,
            "headers": created_headers,
            "action_labels": created_action_labels
        }
        return combined_result

    async def update(self, db: Session, model_id: int, model_request):
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(
            db, Model, model_request, unique_fields, model_id)
        
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            current_time = datetime.now()
            for field in required_fields:
                setattr(db_model, field, getattr(model_request, field))
            db_model.updated_at = current_time
            db.commit()
            db.refresh(db_model)
            
            # Clear existing fields, headers, and action labels
            db.query(ModelFieldRepo.model).filter(
                ModelFieldRepo.model.model_builder_id == model_id).delete()
            db.query(ModelHeaderRepo.model).filter(
                ModelHeaderRepo.model.model_builder_id == model_id).delete()
            db.query(ActionLabelRepo.model).filter(
                ActionLabelRepo.model.model_builder_id == model_id).delete()
            db.commit()
            
            # Store updated fields, headers, and action labels
            created_fields = []
            for field in model_request.fields:
                field.model_builder_id = model_id
                created_field = await ModelFieldRepo().create(db, field)
                created_fields.append(created_field)
            
            created_headers = []
            for header in model_request.headers:
                header.model_builder_id = model_id
                created_header = await ModelHeaderRepo().create(db, header)
                created_headers.append(created_header)
            
            created_action_labels = []
            for action_label in model_request.actionLabels:
                action_label.model_builder_id = model_id
                created_action_label = await ActionLabelRepo().create(db, action_label)
                created_action_labels.append(created_action_label)

            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            
            # Convert the model to a dictionary
            model_data = {column.name: getattr(db_model, column.name) for column in db_model.__table__.columns}

            # Combine and return the updated model with its related objects
            combined_result = {
                **model_data,
                "fields": created_fields,
                "headers": created_headers,
                "action_labels": created_action_labels
            }
            return combined_result
        
        return ResponseHelper.handle_not_found_error(model_id)
    
    @staticmethod
    def get(db: Session, model_id: int):
        print('model_id, mod', model_id)
        return db.query(Model). \
            options(
                joinedload(Model.fields),
                joinedload(Model.action_labels),
                joinedload(Model.headers)
        ). \
            filter(Model.id == model_id). \
            first()

    def get_page_by_name(db: Session, name_singular: str):
        return db.query(ModelBuilderRepo).filter(ModelBuilderRepo.name_singular == name_singular).first()

    def get_page_by_table_name(db: Session, table_name_singular: str):
        return db.query(ModelBuilderRepo).filter(ModelBuilderRepo.table_name_singular == table_name_singular).first()
    
    def get_page_by_table_name_plural(db: Session, table_name_plural: str):
        return db.query(ModelBuilderRepo).filter(ModelBuilderRepo.table_name_plural == table_name_plural).first()

    def get_page_by_apiEndpoint(db: Session, apiEndpoint: str):
        return db.query(ModelBuilderRepo).filter(ModelBuilderRepo.apiEndpoint == apiEndpoint).first()