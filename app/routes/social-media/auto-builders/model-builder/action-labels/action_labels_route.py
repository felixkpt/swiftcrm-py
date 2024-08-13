
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.auto_builders.model_builder.action_labels.action_label_repo import ActionLabelRepo as Repo
from app.requests.schemas.auto_builders.model_builder.action_labels.action_label_schema import ActionLabelSchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new Action_label instance.
@router.post("/", response_model=ModelSchema)
async def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return await repo.create(db=db, model_request=modelRequest)

# Retrieve a list of Action_labels.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single Action_label by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Action_label not found")
    return result

# Update an existing Action_label by ID.
@router.put("/{model_id}", response_model=ModelSchema)
async def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Action_label not found")
    return await repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to Action_labels.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Action_label by ID.
@router.put("/{model_id}/status/{status_id}")
async def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Action_label not found")
    return await repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Action_labels.
@router.put("/statuses")
async def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = await repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Action_label not found")
    return result

# Delete a Action_label by ID.
@router.delete("/{model_id}")
async def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Action_label not found")
    return await repo.delete(db=db, model_id=model_id)
