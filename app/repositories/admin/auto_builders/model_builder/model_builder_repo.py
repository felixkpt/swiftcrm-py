from datetime import datetime
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
        search_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        query = apply_common_filters(db.query(Model), Model, search_fields, query_params)
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
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
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
            for field in model_request.fields:
                await ModelFieldRepo().create(db, new_model.id, field)
            for header in model_request.headers:
                await ModelHeaderRepo().create(db, new_model.id, header)
            for action_label in model_request.actionLabels:
                await ActionLabelRepo().create(db, new_model.id, action_label)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        return new_model

    async def update(self, db: Session, model_id: int, model_request):
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        db_model = db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            current_time = datetime.now()
            for field in required_fields:
                setattr(db_model, field, getattr(model_request, field))
            db_model.updated_at = current_time
            db.commit()
            db.refresh(db_model)
            # Clear existing fields, headers, and action labels
            db.query(ModelFieldRepo.model).filter(ModelFieldRepo.model.auto_page_builder_id == model_id).delete()
            db.query(ModelHeaderRepo.model).filter(ModelHeaderRepo.model.auto_page_builder_id == model_id).delete()
            db.query(ActionLabelRepo.model).filter(ActionLabelRepo.model.auto_page_builder_id == model_id).delete()
            db.commit()
            # Store updated fields, headers, and action labels
            for field in model_request.fields:
                await ModelFieldRepo().create(db, model_id, field)
            for header in model_request.headers:
                await ModelHeaderRepo().create(db, model_id, header)
            for action_label in model_request.actionLabels:
                await ActionLabelRepo().create(db, model_id, action_label)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_model
        return ResponseHelper.handle_not_found_error(model_id)
