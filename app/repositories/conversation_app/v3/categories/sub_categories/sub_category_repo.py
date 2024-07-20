
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation_app.v3.categories.sub_categories.sub_category import ConversationAppV3CategoriesSubCategory as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, add_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo


class SubCategoryRepo(BaseRepo):
    
    model = Model

    async def list(db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['name', 'category_id', 'learn_instructions']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)

        value = query_params.get('category_id', None)
        if value is not None:
            query = query.filter(Model.category_id == value)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        metadata = add_metadata(query, query_params)
        
        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def create(db: Session, model_request):
        required_fields = ['name', 'category_id', 'learn_instructions']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            name=model_request.name,
            category_id=model_request.category_id,
            learn_instructions=model_request.learn_instructions,
        )
        db.add(db_query)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    def update(db: Session, model_id: int, model_request):
        required_fields = ['name', 'category_id', 'learn_instructions']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.name = model_request.name
            db_query.category_id = model_request.category_id
            db_query.learn_instructions = model_request.learn_instructions
            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

