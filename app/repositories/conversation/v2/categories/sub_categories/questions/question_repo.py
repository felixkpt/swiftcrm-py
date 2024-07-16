
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation.v2.categories.sub_categories.questions.question import ConversationV2CategoriesSubCategoriesQuestion as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.repositories.conversation.v2.categories.sub_categories.sub_category_repo import SubCategoryRepo
# Importing functions for querying, searching and sorting
from app.services.search_repo import get_query_params, apply_search_and_sort
# Importing ResponseHelper for consistent error handling
from app.requests.response.response_helper import ResponseHelper


class QuestionRepo:

    @staticmethod
    async def list(db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['category_id', 'sub_category_id', 'question', 'marks']

        query = db.query(Model)
        query = apply_search_and_sort(
            query, Model, search_fields, query_params)

        value = query_params.get('category_id', None)
        if value is not None:
            query = query.filter(Model.category_id == value)
        value = query_params.get('sub_category_id', None)
        if value is not None:
            query = query.filter(Model.sub_category_id == value)

        skip = (query_params['page'] - 1) * query_params['limit']
        query = query.offset(skip).limit(query_params['limit'])

        return query.all()

    @staticmethod
    def get(db: Session, model_id: int):
        result = db.query(Model).filter(Model.id == model_id).first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    @staticmethod
    def create(db: Session, model_request):
        required_fields = ['category_id',
                           'sub_category_id', 'question', 'marks']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(
            db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            category_id=model_request.category_id,
            sub_category_id=model_request.sub_category_id,
            question=model_request.question,
            marks=model_request.marks,
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
        required_fields = ['category_id',
                           'sub_category_id', 'question', 'marks']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(
            db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.category_id = model_request.category_id
            db_query.sub_category_id = model_request.sub_category_id
            db_query.question = model_request.question
            db_query.marks = model_request.marks
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

    @staticmethod
    def get_sub_cat_questions(db, sub_cat_id: int):
        query = db.query(Model).filter(
            Model.sub_category_id == sub_cat_id,
            Model.status_id == 1
        ).all()

        sub_cat_name = SubCategoryRepo.get(
            db, sub_cat_id).name if query else None

        metadata = {
            'title': f'{sub_cat_name} questions list' if sub_cat_name else None,
            'total_count': len(query)
        }

        response = {
            'results': query,
            'metadata': metadata
        }

        return response
