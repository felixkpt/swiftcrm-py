
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.categories2 import Categories2 as Model

class Categories2Repo:

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Model).offset(skip).limit(limit).all()

    @staticmethod
    def get(db: Session, model_id: int):
        return db.query(Model).filter(Model.id == model_id).first()

    @staticmethod
    def create(db: Session, model_request):
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            name=model_request.name,
            description=model_request.description,
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)
        return db_query

    @staticmethod
    def update(db: Session, model_id: int, model_request):
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.name = model_request.name
            db_query.description = model_request.description
        db.commit()
        db.refresh(db_query)
        return db_query

    @staticmethod
    def delete(db: Session, model_id: int):
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            return True
        return False
