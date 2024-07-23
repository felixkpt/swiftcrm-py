from sqlalchemy.orm import Session
from app.requests.response.response_helper import ResponseHelper
from app.auth import user  # Import user function

class BaseRepo:

    model = None
    notification = None  # Ensure this is set in derived classes if needed

    def get(self, db: Session, model_id: int, request=None):
        current_user_id = user(request).id
        result = db.query(self.model).filter(
            self.model.id == model_id,
            self.model.user_id == current_user_id
        ).first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    async def update_status(self, db: Session, model_id: int, status_id: int, request=None):
        current_user_id = user(request).id
        db_query = db.query(self.model).filter(
            self.model.id == model_id,
            self.model.user_id == current_user_id
        ).first()
        if db_query:
            db_query.status_id = status_id
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Record status updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    async def update_multiple_statuses(self, db: Session, model_ids: list[int], status_id: int, request=None):
        current_user_id = user(request).id
        db_query = db.query(self.model).filter(
            self.model.id.in_(model_ids),
            self.model.user_id == current_user_id
        ).all()
        if db_query:
            for record in db_query:
                record.status_id = status_id
            db.commit()
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Records statuses updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_ids)

    async def archive(self, db: Session, model_id: int, archive_db: Session, request=None):
        current_user_id = user(request).id
        db_query = db.query(self.model).filter(
            self.model.id == model_id,
            self.model.user_id == current_user_id
        ).first()
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
        current_user_id = user(request).id
        db_query = db.query(self.model).filter(
            self.model.id == model_id,
            self.model.user_id == current_user_id
        ).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            await self.notification.notify_model_updated(db, self.model.__tablename__, 'Record deleted!')
            return {"message": "Record deleted successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)
