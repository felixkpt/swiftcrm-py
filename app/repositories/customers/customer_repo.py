
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.customers.customer_model import Customer as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function
import time
class CustomerRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        start_time = time.time()
        query_params = get_query_params(request)
        search_fields = ['first_name', 'last_name', 'phone_number', 'email', 'alternate_number']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        
        query,search_fields = self.repo_specific_filters(query, Model, search_fields, query_params)
        metadata = set_metadata(query, query_params)

        # Get current user ID
        current_user_id = user(request).id
        # query = query.filter(Model.user_id == current_user_id)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        end_time = time.time()

        loading_time = end_time - start_time
        metadata['loading_time'] = str(round(loading_time, 2)) + ' secs'

        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, search_fields, query_params):
        value = query_params.get('first_name', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.first_name.ilike(f'%{value}%'))
        value = query_params.get('last_name', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.last_name.ilike(f'%{value}%'))
        value = query_params.get('phone_number', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.phone_number.ilike(f'%{value}%'))
        value = query_params.get('email', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.email.ilike(f'%{value}%'))
        value = query_params.get('alternate_number', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.alternate_number.ilike(f'%{value}%'))
        value = query_params.get('user_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.user_id == int(value))

        return query,search_fields

    async def create(self, db: Session, model_request):
        required_fields = ['first_name', 'last_name', 'phone_number', 'email', 'alternate_number']
        unique_fields = ['phone_number', 'email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
            first_name = str(model_request.first_name).strip(),
            last_name = str(model_request.last_name).strip(),
            phone_number = str(model_request.phone_number).strip(),
            email = str(model_request.email).strip(),
            alternate_number = str(model_request.alternate_number).strip(),
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
        required_fields = ['first_name', 'last_name', 'phone_number', 'email', 'alternate_number']
        unique_fields = ['phone_number', 'email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
            db_query.first_name = str(model_request.first_name).strip()
            db_query.last_name = str(model_request.last_name).strip()
            db_query.phone_number = str(model_request.phone_number).strip()
            db_query.email = str(model_request.email).strip()
            db_query.alternate_number = str(model_request.alternate_number).strip()
            db_query.user_id = current_user_id
            db_query.updated_at = current_time
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
