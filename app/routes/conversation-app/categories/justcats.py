from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories.justcat_repo import JustcatRepo as Repo
from app.requests.schemas.justcat import JustcatSchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return Repo.create(db=db, model_request=modelRequest)

@router.get("/")
def list_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = Repo.list(db, skip=skip, limit=limit)
    return results

@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Justcat not found")
    return result

@router.put("/{model_id}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Justcat not found")
    return Repo.update(db=db, model_id=model_id, model_request=modelRequest)

@router.delete("/{model_id}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Justcat not found")
    return Repo.delete(db=db, model_id=model_id)
