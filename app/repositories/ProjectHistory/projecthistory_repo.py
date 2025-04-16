
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.ProjectHistory.projecthistory_model import Projecthistory as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function
import time

class ProjecthistoryRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        start_time = time.time()
        
        query_params = get_query_params(request)
        search_fields = ['id', 'project__name_']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)

        # Get current user ID
        current_user_id = user(request).id
        query = query.filter(Model.user_id == current_user_id)
        metadata = set_metadata(query, query_params)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        end_time = time.time()
        loading_time = end_time - start_time
        metadata['loading_time'] = str(round(loading_time, 2))+' secs'

        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):
        value = query_params.get('project__name_', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.project__name_.ilike(f'%{value}%'))
        value = query_params.get('user_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.user_id == int(value))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['project__name_']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
            project__name_ = str(model_request.project__name_).strip(),
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
        required_fields = ['project__name_']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
            db_query.project__name_ = str(model_request.project__name_).strip()
            db_query.user_id = current_user_id
            db_query.updated_at = current_time
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
