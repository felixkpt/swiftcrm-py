# app/repositories/base_repo.py

from sqlalchemy.orm import Session
from app.requests.response.response_helper import ResponseHelper

class BaseRepo:
    
    model = None

    @classmethod
    def get(cls, db: Session, model_id: int):
        result = db.query(cls.model).filter(cls.model.id == model_id).first()
        if not result:
            return ResponseHelper.handle_not_found_error(model_id)
        return result

    @classmethod
    def delete(cls, db: Session, model_id: int):
        db_query = db.query(cls.model).filter(cls.model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            return {"message": "Record deleted successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    @classmethod
    def update_status(cls, db: Session, model_id: int, status_id: int):
        db_query = db.query(cls.model).filter(cls.model.id == model_id).first()
        if db_query:
            db_query.status_id = status_id
            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)

    @classmethod
    def update_multiple_statuses(cls, db: Session, model_ids: list[int], status_id: int):
        db_query = db.query(cls.model).filter(cls.model.id.in_(model_ids)).all()
        if db_query:
            for record in db_query:
                record.status_id = status_id
            db.commit()
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_ids)

    @classmethod
    def archive(cls, db: Session, model_id: int, archive_db: Session):
        db_query = db.query(cls.model).filter(cls.model.id == model_id).first()
        if db_query:
            archive_db.add(db_query)
            db.delete(db_query)
            db.commit()
            archive_db.commit()
            return {"message": "Record archived successfully"}
        else:
            return ResponseHelper.handle_not_found_error(model_id)
