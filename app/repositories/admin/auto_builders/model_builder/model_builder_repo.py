
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.auto_builders.model_builder.model_builder import AdminAutoBuildersModelBuilder as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService  # Import NotificationService


class ModelBuilderRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()  # Instantiate notification class

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint']

        query = db.query(Model)
        
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        
        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):

        value = query_params.get('name_singular', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.name_singular.ilike(f'%{value}%'))
        value = query_params.get('name_plural', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.name_plural.ilike(f'%{value}%'))
        value = query_params.get('modelURI', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.modelURI.ilike(f'%{value}%'))
        value = query_params.get('apiEndpoint', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.apiEndpoint.ilike(f'%{value}%'))
        value = query_params.get('table_name_singular', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.table_name_singular.ilike(f'%{value}%'))
        value = query_params.get('table_name_plural', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.table_name_plural.ilike(f'%{value}%'))
        value = query_params.get('class_name', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.class_name.ilike(f'%{value}%'))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            name_singular=model_request.name_singular,
            name_plural=model_request.name_plural,
            modelURI=model_request.modelURI,
            apiEndpoint=model_request.apiEndpoint,
            table_name_singular=model_request.table_name_singular,
            table_name_plural=model_request.table_name_plural,
            class_name=model_request.class_name,
        )
        db.add(db_query)
        try:
            db.commit()
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    async def update(self, db: Session, model_id: int, model_request):
        required_fields = ['name_singular', 'name_plural', 'modelURI', 'apiEndpoint']
        unique_fields = ['table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.name_singular = model_request.name_singular
            db_query.name_plural = model_request.name_plural
            db_query.modelURI = model_request.modelURI
            db_query.apiEndpoint = model_request.apiEndpoint
            db_query.table_name_singular = model_request.table_name_singular
            db_query.table_name_plural = model_request.table_name_plural
            db_query.class_name = model_request.class_name
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
