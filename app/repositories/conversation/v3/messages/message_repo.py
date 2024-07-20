
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation.v3.messages.message import ConversationV3Message as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_filters, add_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo


class MessageRepo(BaseRepo):
    
    model = Model

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['user_id', 'category_id', 'sub_category_id', 'role', 'mode', 'interview_id', 'question_id', 'question_scores', 'content', 'audio_uri']

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
        value = query_params.get('interview_id', None)
        if value is not None:
            query = query.filter(Model.interview_id == value)
        value = query_params.get('question_id', None)
        if value is not None:
            query = query.filter(Model.question_id == value)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        metadata = add_metadata(query, query_params)
        
        results = {
            "data": query.all(),
            "metadata": metadata
        }

        return results

    def create(self, db: Session, model_request):
        required_fields = ['user_id', 'category_id', 'sub_category_id', 'role', 'mode', 'interview_id', 'question_id', 'question_scores', 'content', 'audio_uri']
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
            role=model_request.role,
            mode=model_request.mode,
            interview_id=model_request.interview_id,
            question_id=model_request.question_id,
            question_scores=model_request.question_scores,
            content=model_request.content,
            audio_uri=model_request.audio_uri,
        )
        db.add(db_query)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    def update(self, db: Session, model_id: int, model_request):
        required_fields = ['user_id', 'category_id', 'sub_category_id', 'role', 'mode', 'interview_id', 'question_id', 'question_scores', 'content', 'audio_uri']
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
            db_query.role = model_request.role
            db_query.mode = model_request.mode
            db_query.interview_id = model_request.interview_id
            db_query.question_id = model_request.question_id
            db_query.question_scores = model_request.question_scores
            db_query.content = model_request.content
            db_query.audio_uri = model_request.audio_uri
            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

