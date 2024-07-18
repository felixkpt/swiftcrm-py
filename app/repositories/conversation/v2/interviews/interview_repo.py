
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation.v2.interviews.interview import ConversationV2Interview as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_filters  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling

class InterviewRepo:

    @staticmethod
    async def list(db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['user_id', 'category_id', 'sub_category_id', 'question_id', 'scores', 'max_scores', 'percentage_score']

        query = db.query(Model)
        query = apply_filters(query, Model, search_fields, query_params)

        value = query_params.get('user_id', None)
        if value is not None:
            query = query.filter(Model.user_id == value)
        value = query_params.get('category_id', None)
        if value is not None:
            query = query.filter(Model.category_id == value)
        value = query_params.get('sub_category_id', None)
        if value is not None:
            query = query.filter(Model.sub_category_id == value)
        value = query_params.get('question_id', None)
        if value is not None:
            query = query.filter(Model.question_id == value)

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
        required_fields = ['user_id', 'category_id', 'sub_category_id', 'question_id', 'scores', 'max_scores', 'percentage_score']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            user_id=model_request.user_id,
            category_id=model_request.category_id,
            sub_category_id=model_request.sub_category_id,
            question_id=model_request.question_id,
            scores=model_request.scores,
            max_scores=model_request.max_scores,
            percentage_score=model_request.percentage_score,
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
        required_fields = ['user_id', 'category_id', 'sub_category_id', 'question_id', 'scores', 'max_scores', 'percentage_score']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.user_id = model_request.user_id
            db_query.category_id = model_request.category_id
            db_query.sub_category_id = model_request.sub_category_id
            db_query.question_id = model_request.question_id
            db_query.scores = model_request.scores
            db_query.max_scores = model_request.max_scores
            db_query.percentage_score = model_request.percentage_score
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
