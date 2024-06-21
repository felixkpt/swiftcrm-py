from sqlalchemy.orm import Session
from app.database.connection.string import String
from app.requests.schemas.string import StringSchema


def get_string(db: Session, string_id: int):
    return db.query(String).filter(String.id == string_id).first()


def get_string(db: Session, skip: int = 0, limit: int = 10):
    return db.query(String).offset(skip).limit(limit).all()


def create_string(db: Session, string: StringSchema):
    db_string = String(
        string=string.string,
    )
    db.add(db_string)
    db.commit()
    db.refresh(db_string)
    return db_string
