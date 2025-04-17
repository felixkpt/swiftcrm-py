
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.modules.api.novels.novel_repo import NovelRepo as Repo
from app.modules.api.novels.novel_schema import NovelSchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new Novel instance.
@router.post("/", response_model=ModelSchema)
async def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return await repo.create(db=db, model_request=modelRequest)

# Retrieve a list of Novels.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single Novel by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Novel not found")
    return result

# Update an existing Novel by ID.
@router.put("/{model_id}", response_model=ModelSchema)
async def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Novel not found")
    return await repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to Novels.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Novel by ID.
@router.put("/{model_id}/status/{status_id}")
async def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Novel not found")
    return await repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Novels.
@router.put("/statuses")
async def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = await repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Novel not found")
    return result

# Delete a Novel by ID.
@router.delete("/{model_id}")
async def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Novel not found")
    return await repo.delete(db=db, model_id=model_id)
