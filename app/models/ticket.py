from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from app.models.base import Base

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(String(255))
    updated_at = Column(String(255))
    source_id = Column(Integer)
    customer_id = Column(Integer)
    disposition_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def list_tickets(db, skip=0, limit=10):
    return db.query(Ticket).offset(skip).limit(limit).all()


def get_ticket(db, ticket_id):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def create_ticket(db, ticket):
    current_time = datetime.now()
    db_ticket = Ticket(
        created_at=current_time,
        updated_at=current_time,
        source_id=ticket.source_id,
        customer_id=ticket.customer_id,
        disposition_id=ticket.disposition_id,
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def update_ticket(db, ticket_id, ticket):
    current_time = datetime.now()
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db_ticket.updated_at = current_time
        db_ticket.source_id = ticket.source_id
        db_ticket.customer_id = ticket.customer_id
        db_ticket.disposition_id = ticket.disposition_id
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def delete_ticket(db, ticket_id):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
        return True
    return False
