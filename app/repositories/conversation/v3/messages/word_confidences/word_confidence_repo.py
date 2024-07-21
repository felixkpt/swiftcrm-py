
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation.v3.messages.word_confidences.word_confidence import ConversationV3MessagesWordConfidence as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo


class WordConfidenceRepo(BaseRepo):
    
    model = Model

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['message_id', 'word', 'start_time_seconds', 'end_time_seconds', 'confidence']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)

        value = query_params.get('message_id', None)
        if value is not None:
            query = query.filter(Model.message_id == value)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        metadata = set_metadata(query, query_params)
        
        results = {
            "data": query.all(),
            "metadata": metadata
        }

        return results

    def create(self, db: Session, model_request):
        required_fields = ['message_id', 'word', 'start_time_seconds', 'end_time_seconds', 'confidence']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            message_id=model_request.message_id,
            word=model_request.word,
            start_time_seconds=model_request.start_time_seconds,
            end_time_seconds=model_request.end_time_seconds,
            confidence=model_request.confidence,
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
        required_fields = ['message_id', 'word', 'start_time_seconds', 'end_time_seconds', 'confidence']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.message_id = model_request.message_id
            db_query.word = model_request.word
            db_query.start_time_seconds = model_request.start_time_seconds
            db_query.end_time_seconds = model_request.end_time_seconds
            db_query.confidence = model_request.confidence
            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

