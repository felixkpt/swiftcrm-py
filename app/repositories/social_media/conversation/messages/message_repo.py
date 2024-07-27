
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.social_media.conversation.messages.message_model import SocialMediaConversationMessage as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function

class MessageRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['category_id', 'sub_category_id', 'role', 'mode', 'content', 'audio_uri']

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        # Get current user ID
        current_user_id = user(request).id
        query = query.filter(Model.user_id == current_user_id)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):
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
        value = query_params.get('audio_uri', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.audio_uri.ilike(f'%{value}%'))
        value = query_params.get('interview_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.interview_id == int(value))
        value = query_params.get('question_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.question_id == int(value))
        value = query_params.get('question_scores', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.question_scores.ilike(f'%{value}%'))
        value = query_params.get('user_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.user_id == int(value))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['category_id', 'sub_category_id', 'role', 'mode', 'content', 'audio_uri']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
            category_id = model_request.category_id,
            sub_category_id = model_request.sub_category_id,
            role = str(model_request.role).strip(),
            mode = str(model_request.mode).strip(),
            content = model_request.content,
            audio_uri = str(model_request.audio_uri).strip(),
            interview_id = model_request.interview_id,
            question_id = model_request.question_id,
            question_scores = model_request.question_scores,
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
        required_fields = ['category_id', 'sub_category_id', 'role', 'mode', 'content', 'audio_uri']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
            db_query.category_id = model_request.category_id
            db_query.sub_category_id = model_request.sub_category_id
            db_query.role = str(model_request.role).strip()
            db_query.mode = str(model_request.mode).strip()
            db_query.content = model_request.content
            db_query.audio_uri = str(model_request.audio_uri).strip()
            db_query.interview_id = model_request.interview_id
            db_query.question_id = model_request.question_id
            db_query.question_scores = model_request.question_scores
            db_query.user_id = current_user_id
            db_query.updated_at = current_time
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
