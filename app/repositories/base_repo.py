# app/repositories/base_repo.py

from sqlalchemy.orm import Session
from app.requests.response.response_helper import ResponseHelper


class BaseRepo:

    model = None

    def get(self, db: Session, model_id: int):
        result = db.query(self.model).filter(
            self.model.id == model_id).first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    async def update_status(self, db: Session, model_id: int, status_id: int):
        db_query = db.query(self.model).filter(
            self.model.id == model_id).first()
        if db_query:
            db_query.status_id = status_id
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(self.model.__tablename__, 'Record was status updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    async def update_multiple_statuses(self, db: Session, model_ids: list[int], status_id: int):
        db_query = db.query(self.model).filter(
            self.model.id.in_(model_ids)).all()
        if db_query:
            for record in db_query:
                record.status_id = status_id
            db.commit()
            await self.notification.notify_model_updated(self.model.__tablename__, 'Records statuses updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_ids)

    async def archive(self, db: Session, model_id: int, archive_db: Session):
        db_query = db.query(self.model).filter(
            self.model.id == model_id).first()
        if db_query:
            archive_db.add(db_query)
            db.delete(db_query)
            db.commit()
            archive_db.commit()
            await self.notification.notify_model_updated(self.model.__tablename__, 'Record was archived!')
            return {"message": "Record archived successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    async def delete(self, db: Session, model_id: int):
        db_query = db.query(self.model).filter(
            self.model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            await self.notification.notify_model_updated(self.model.__tablename__, 'Record was deleted!')
            return {"message": "Record deleted successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)
