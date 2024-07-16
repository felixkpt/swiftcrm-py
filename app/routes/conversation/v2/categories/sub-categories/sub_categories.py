from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.conversation.v2.categories.sub_categories.sub_category_repo import SubCategoryRepo as Repo
from app.requests.schemas.conversation.v2.categories.sub_categories.sub_category import SubCategorySchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return Repo.create(db=db, model_request=modelRequest)

@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await Repo.list(db, request)
    return results

@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sub_category not found")
    return result

@router.put("/{model_id}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sub_category not found")
    return Repo.update(db=db, model_id=model_id, model_request=modelRequest)

@router.put("/{model_id}/status/{status_id}")
def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sub_category not found")
    return Repo.update_status(db=db, model_id=model_id, status_id=status_id)

@router.delete("/{model_id}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Sub_category not found")
    return Repo.delete(db=db, model_id=model_id)
