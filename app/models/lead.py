from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.models.base import Base

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Lead(Base):
    __tablename__ = 'lead'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(String(255))
    updated_at = Column(String(255))
    source_id = Column(Integer)
    customer_id = Column(Integer)
    category_id = Column(Integer)
    sub_category_id = Column(Integer)
    disposition_id = Column(Integer)
    comments = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def list_leads(db, skip=0, limit=10):
    return db.query(Lead).offset(skip).limit(limit).all()


def get_lead(db, lead_id):
    return db.query(Lead).filter(Lead.id == lead_id).first()


def create_lead(db, lead):
    current_time = datetime.now()
    db_lead = Lead(
        created_at=current_time,
        updated_at=current_time,
        source_id=lead.source_id,
        customer_id=lead.customer_id,
        category_id=lead.category_id,
        sub_category_id=lead.sub_category_id,
        disposition_id=lead.disposition_id,
        comments=lead.comments,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def update_lead(db, lead_id, lead):
    current_time = datetime.now()
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        db_lead.updated_at = current_time
        db_lead.source_id = lead.source_id
        db_lead.customer_id = lead.customer_id
        db_lead.category_id = lead.category_id
        db_lead.sub_category_id = lead.sub_category_id
        db_lead.disposition_id = lead.disposition_id
        db_lead.comments = lead.comments
    db.commit()
    db.refresh(db_lead)
    return db_lead


def delete_lead(db, lead_id):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        db.delete(db_lead)
        db.commit()
        return True
    return False
