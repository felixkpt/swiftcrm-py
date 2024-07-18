from app.services.auto_model.saves_file import handler

def generate_routes(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_slugged = data['api_endpoint_slugged']
    model_name_pascal = data['model_name_pascal']
    name_singular = data['name_singular']
    name_plural = data['name_plural']

    # Define CRUD routes for the specified model
    content = f"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.{api_endpoint_slugged+'.'+name_singular.lower()}_repo import {model_name_pascal}Repo as Repo
from app.requests.schemas.{api_endpoint_slugged+'.'+name_singular.lower()} import {model_name_pascal}Schema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new {name_singular} instance.
@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return repo.create(db=db, model_request=modelRequest)

# Retrieve a list of {name_plural}.
@router.get("/")
async def list_route(request: Request, db: Session = get_db):
    results = await repo.list(db, request)
    return results

# Retrieve a single {name_singular} by ID.
@router.get("/{{model_id}}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{name_singular} not found")
    return result

# Update an existing {name_singular} by ID.
@router.put("/{{model_id}}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{name_singular} not found")
    return repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to {name_plural}.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a {name_singular} by ID.
@router.put("/{{model_id}}/status/{{status_id}}")
def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{name_singular} not found")
    return repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple {name_plural}.
@router.put("/statuses")
def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{name_singular} not found")
    return result

# Delete a {name_singular} by ID.
@router.delete("/{{model_id}}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{name_singular} not found")
    return repo.delete(db=db, model_id=model_id)
"""

    filename = f'{name_plural.lower()}.py'
    handler(api_endpoint, 'routes', filename, content)
