
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.customers.customer import Customer as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService  # Import NotificationService


class CustomerRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()  # Instantiate notification class

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['name', 'email', 'phone_number']

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

        value = query_params.get('name', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.name.ilike(f'%{value}%'))
        value = query_params.get('email', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.email.ilike(f'%{value}%'))
        value = query_params.get('phone_number', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.phone_number.ilike(f'%{value}%'))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['name', 'email', 'phone_number']
        unique_fields = ['email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at = current_time,
            updated_at = current_time,
            name = str(model_request.name).strip(),
            email = str(model_request.email).strip(),
            phone_number = str(model_request.phone_number).strip(),
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
        required_fields = ['name', 'email', 'phone_number']
        unique_fields = ['email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.name = str(model_request.name).strip()
            db_query.email = str(model_request.email).strip()
            db_query.phone_number = str(model_request.phone_number).strip()
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
