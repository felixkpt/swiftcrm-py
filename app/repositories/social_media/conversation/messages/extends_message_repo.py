from sqlalchemy.orm import Session
from app.repositories.base_repo import BaseRepo
from sqlalchemy.exc import SQLAlchemyError
from app.requests.response.response_helper import ResponseHelper
from app.repositories.social_media.conversation.shared import SharedRepo


class ExtendsMessageRepo():
    def get_cat_conversation(self, db: Session, cat_id: int, mode: str = 'training'):
        if mode not in ['training', 'interview']:
            raise ValueError("Mode must be either 'training' or 'interview'")

        try:
            query = db.query(self.model).filter(
                self.model.category_id == cat_id,
                self.model.mode == mode,
                self.model.status_id == 1
            )
            return query.all()
        except SQLAlchemyError as e:
            return ResponseHelper.handle_database_error(e)

    async def get_sub_cat_conversation(self, db: Session, request, sub_cat_id: int, mode: str = 'training', interview_id: int = None):
        if mode not in ['training', 'interview']:
            raise ValueError("Mode must be either 'training' or 'interview'")

        try:
            query = db.query(self.model).filter(
                self.model.sub_category_id == sub_cat_id,
                self.model.mode == mode,
                self.model.status_id == 1
            )
            if interview_id and int(interview_id) > 0:
                query = query.filter(self.model.interview_id == interview_id)
            else:
                query = query.filter(self.model.interview_id.is_(None))

            results = query.order_by(self.model.id.asc()).all()

            metadata = {
                'title': 'Conversation list',
                'total_count': len(results),
            }

            if mode == 'interview' and interview_id:
                progress = await SharedRepo.interview_progress(
                    db, request, interview_id, sub_cat_id)
                metadata['question_number'] = progress.get(
                    'question_number', 0)
                metadata['is_completed'] = progress.get('is_completed', False)

            response = {
                'records': results,
                'metadata': metadata
            }

            return response

        except SQLAlchemyError as e:
            return ResponseHelper.handle_database_error(e)
