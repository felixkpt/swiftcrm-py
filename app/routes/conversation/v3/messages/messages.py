
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.conversation.v3.messages.message_repo import MessageRepo as Repo
from app.requests.schemas.conversation.v3.messages.message import MessageSchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new Message instance.
@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return repo.create(db=db, model_request=modelRequest)

# Retrieve a list of Messages.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single Message by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Message not found")
    return result

# Update an existing Message by ID.
@router.put("/{model_id}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Message not found")
    return repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to Messages.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Message by ID.
@router.put("/{model_id}/status/{status_id}")
def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Message not found")
    return repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Messages.
@router.put("/statuses")
def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Message not found")
    return result

# Delete a Message by ID.
@router.delete("/{model_id}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Message not found")
    return repo.delete(db=db, model_id=model_id)
