
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.conversation.v3.categories.sub_categories.sub_category_repo import SubCategoryRepo as Repo
from app.requests.schemas.conversation.v3.categories.sub_categories.sub_category import SubCategorySchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new Sub_category instance.
@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return repo.create(db=db, model_request=modelRequest)

# Retrieve a list of Sub_categories.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single Sub_category by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sub_category not found")
    return result

# Update an existing Sub_category by ID.
@router.put("/{model_id}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sub_category not found")
    return repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to Sub_categories.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Sub_category by ID.
@router.put("/{model_id}/status/{status_id}")
def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sub_category not found")
    return repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Sub_categories.
@router.put("/statuses")
def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sub_category not found")
    return result

# Delete a Sub_category by ID.
@router.delete("/{model_id}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Sub_category not found")
    return repo.delete(db=db, model_id=model_id)
