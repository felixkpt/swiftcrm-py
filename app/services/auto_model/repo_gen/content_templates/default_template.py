def get_default_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2):
    content = f"""
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.{api_endpoint_slugged}.{model_path_name} import {class_name} as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function

class {model_name_pascal}Repo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        # Get current user ID
        current_user_id = user(request).id
        query = query.filter(Model.user_id == current_user_id)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        results = {{
            "records": query.all(),
            "metadata": metadata
        }}

        return results

    def repo_specific_filters(self, query, Model, query_params):
{repo_specific_filters}
        return query

    async def create(self, db: Session, model_request):
        required_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}
        unique_fields = {[field['name'] for field in fields if field.get('isUnique', False)]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
{inserts_args1}        )
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
        required_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}
        unique_fields = {[field['name'] for field in fields if field.get('isUnique', False)]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
{inserts_args2}            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
"""
    return content