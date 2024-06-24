from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import ticket as model
from app.requests.schemas import ticket as schema
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=schema.TicketSchema)
def create_ticket(ticket: schema.TicketSchema, db: Session = Depends(get_db)):
    return model.create_ticket(db=db, ticket=ticket)

@router.get("/")
def read_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ticket = model.list_tickets(db, skip=skip, limit=limit)
    return ticket

@router.get("/{ticket_id}")
def view_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = model.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=schema.TicketSchema)
def update_ticket(ticket_id: int, ticket: schema.TicketSchema, db: Session = Depends(get_db)):
    db_ticket = model.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return model.update_ticket(db=db, ticket_id=ticket_id, ticket=ticket)

@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = model.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return model.delete_ticket(db=db, id=ticket_id)
