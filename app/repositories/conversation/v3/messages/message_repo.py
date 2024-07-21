
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.conversation.v3.messages.message import ConversationV3Message as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, add_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService  # Import NotificationService


class MessageRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()  # Instantiate notification class

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['user_id', 'category_id', 'sub_category_id', 'role', 'mode', 'interview_id', 'question_id', 'question_scores', 'content', 'audio_uri']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        metadata = add_metadata(query, query_params)
        
        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):

        value = query_params.get('user_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.user_id == int(value))
        value = query_params.get('category_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.category_id == int(value))
        value = query_params.get('sub_category_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.sub_category_id == int(value))
        value = query_params.get('role', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.role.ilike(f'%{value}%'))
        value = query_params.get('mode', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.mode.ilike(f'%{value}%'))
        value = query_params.get('interview_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.interview_id == int(value))
        value = query_params.get('question_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.question_id == int(value))
        value = query_params.get('question_scores', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.question_scores.ilike(f'%{value}%'))
        value = query_params.get('audio_uri', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.audio_uri.ilike(f'%{value}%'))

        return query

    async def create(self, db: Session, model_request):
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
            await self.notification.notify_model_updated(Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    async def update(self, db: Session, model_id: int, model_request):
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
            await self.notification.notify_model_updated(Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
