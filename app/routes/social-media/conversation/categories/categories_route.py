
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.social_media.conversation.categories.category_repo import CategoryRepo as Repo
from app.requests.schemas.social_media.conversation.categories.category_schema import CategorySchema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new Category instance.
@router.post("/", response_model=ModelSchema)
async def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return await repo.create(db=db, model_request=modelRequest)

# Retrieve a list of Categories.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    print('CATS Source:-->',request.query_params.get('source', None))

    results = await repo.list(db, request)
    return results

# Retrieve a single Category by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category not found")
    return result

# Update an existing Category by ID.
@router.put("/{model_id}", response_model=ModelSchema)
async def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category not found")
    return await repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to Categories.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Category by ID.
@router.put("/{model_id}/status/{status_id}")
async def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category not found")
    return await repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Categories.
@router.put("/statuses")
async def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = await repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category not found")
    return result

# Delete a Category by ID.
@router.delete("/{model_id}")
async def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Category not found")
    return await repo.delete(db=db, model_id=model_id)
