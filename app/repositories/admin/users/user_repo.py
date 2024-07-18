
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.users.user import AdminUser as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_filters  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling

class UserRepo:

    @staticmethod
    async def list(db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['username', 'email', 'password']

        query = db.query(Model)
        query = apply_filters(query, Model, search_fields, query_params)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        return query.all()

    @staticmethod
    def get(db: Session, model_id: int):
        result = db.query(Model).filter(Model.id == model_id).first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    @staticmethod
    def create(db: Session, model_request):
        required_fields = ['username', 'email', 'password']
        unique_fields = ['email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            username=model_request.username,
            email=model_request.email,
            password=model_request.password,
        )
        db.add(db_query)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    @staticmethod
    def update(db: Session, model_id: int, model_request):
        required_fields = ['username', 'email', 'password']
        unique_fields = ['email']
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.username = model_request.username
            db_query.email = model_request.email
            db_query.password = model_request.password
            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    @staticmethod
    def delete(db: Session, model_id: int):
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            return {"message": "Record deleted successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)
