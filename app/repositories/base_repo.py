from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from app.requests.response.response_helper import ResponseHelper
from app.auth import user  # Import user function
import inspect

class BaseRepo:

    model = None
    notification = None  # Ensure this is set in derived classes if needed

    @staticmethod
    def _user_can_view_all(model, method, user):
        # Define logic to determine if the user can view the model
        # For now, it returns False, adjust as needed
        return False

    def _apply_user_filter(self, query, user):
        method = self._get_caller()
        if self._user_can_view_all(self.model, method, user) or 'user_id' in [c.name for c in inspect(self.model).c]:
            query = query.filter(self.model.user_id == user.id)
        return query

    @staticmethod
    def _get_caller():
        # Get the name of the caller method
        return inspect.stack()[2].function

    def get(self, db: Session, model_id: int, request=None):
        current_user = user(request)
        query = db.query(self.model).filter(self.model.id == model_id)
        query = self._apply_user_filter(query, current_user)
        result = query.first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    async def update_status(self, db: Session, model_id: int, status_id: int, request=None):
        current_user = user(request)
        query = db.query(self.model).filter(self.model.id == model_id)
        query = self._apply_user_filter(query, current_user)
        db_query = query.first()
        if db_query:
            db_query.status_id = status_id
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Record status updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    async def update_multiple_statuses(self, db: Session, model_ids: list[int], status_id: int, request=None):
        current_user = user(request)
        query = db.query(self.model).filter(self.model.id.in_(model_ids))
        query = self._apply_user_filter(query, current_user)
        db_query = query.all()
        if db_query:
            for record in db_query:
                record.status_id = status_id
            db.commit()
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Records statuses updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_ids)

    async def archive(self, db: Session, model_id: int, archive_db: Session, request=None):
        current_user = user(request)
        query = db.query(self.model).filter(self.model.id == model_id)
        query = self._apply_user_filter(query, current_user)
        db_query = query.first()
        if db_query:
            archive_db.add(db_query)
            db.delete(db_query)
            db.commit()
            archive_db.commit()
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Record archived!')
            return {"message": "Record archived successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    async def delete(self, db: Session, model_id: int, request=None):
        current_user = user(request)
        query = db.query(self.model).filter(self.model.id == model_id)
        query = self._apply_user_filter(query, current_user)
        db_query = query.first()
        if db_query:
            db.delete(db_query)
            db.commit()
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Record deleted!')
            return {"message": "Record deleted successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)
