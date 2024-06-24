from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import lead as model
from app.requests.schemas import lead as schema
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=schema.LeadSchema)
def create_lead(lead: schema.LeadSchema, db: Session = Depends(get_db)):
    return model.create_lead(db=db, lead=lead)

@router.get("/")
def read_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    lead = model.list_leads(db, skip=skip, limit=limit)
    return lead

@router.get("/{lead_id}")
def view_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = model.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.put("/{lead_id}", response_model=schema.LeadSchema)
def update_lead(lead_id: int, lead: schema.LeadSchema, db: Session = Depends(get_db)):
    db_lead = model.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return model.update_lead(db=db, lead_id=lead_id, lead=lead)

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = model.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return model.delete_lead(db=db, id=lead_id)
