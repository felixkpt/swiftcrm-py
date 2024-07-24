
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.auto_builders.model_builders2.model_builder2_model import AdminAutoBuildersModelBuilders2ModelBuilder2 as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function

class ModelBuilder2Repo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['uuid', 'modelDisplayName', 'name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        # Get current user ID
        current_user_id = user(request).id
        query = query.filter(Model.user_id == current_user_id)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):

        value = query_params.get('uuid', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.uuid.ilike(f'%{value}%'))
        value = query_params.get('modelDisplayName', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.modelDisplayName.ilike(f'%{value}%'))
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
        value = query_params.get('user_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.user_id == int(value))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['uuid', 'modelDisplayName', 'name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        unique_fields = ['modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
            uuid = str(model_request.uuid).strip(),
            modelDisplayName = str(model_request.modelDisplayName).strip(),
            name_singular = str(model_request.name_singular).strip(),
            name_plural = str(model_request.name_plural).strip(),
            modelURI = str(model_request.modelURI).strip(),
            apiEndpoint = str(model_request.apiEndpoint).strip(),
            table_name_singular = str(model_request.table_name_singular).strip(),
            table_name_plural = str(model_request.table_name_plural).strip(),
            class_name = str(model_request.class_name).strip(),
            user_id = current_user_id,
            created_at = current_time,
            updated_at = current_time,
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
        required_fields = ['uuid', 'modelDisplayName', 'name_singular', 'name_plural', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural', 'class_name']
        unique_fields = ['modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
            db_query.uuid = str(model_request.uuid).strip()
            db_query.modelDisplayName = str(model_request.modelDisplayName).strip()
            db_query.name_singular = str(model_request.name_singular).strip()
            db_query.name_plural = str(model_request.name_plural).strip()
            db_query.modelURI = str(model_request.modelURI).strip()
            db_query.apiEndpoint = str(model_request.apiEndpoint).strip()
            db_query.table_name_singular = str(model_request.table_name_singular).strip()
            db_query.table_name_plural = str(model_request.table_name_plural).strip()
            db_query.class_name = str(model_request.class_name).strip()
            db_query.user_id = current_user_id
            db_query.updated_at = current_time
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
