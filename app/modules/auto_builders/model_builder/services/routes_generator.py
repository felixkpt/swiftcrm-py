from app.modules.auto_builders.model_builder.services.saves_file import handler
from app.modules.auto_builders.model_builder.services.helpers import build_dot_namespace

def generate_routes(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_dotnotation = data['api_endpoint_dotnotation']
    model_name_pascal = data['model_name_pascal']
    nameSingular = data['nameSingular'].replace('-', '_')
    namePlural = data['namePlural']

    customs = ['model_builder']

    if nameSingular.replace('-', '_').lower() in customs:
        return

    # Define CRUD routes for the specified model
    content = f"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.modules.{build_dot_namespace(api_endpoint_dotnotation, nameSingular.lower())}_repo import {model_name_pascal}Repo as Repo
from app.modules.{build_dot_namespace(api_endpoint_dotnotation, nameSingular.lower())}_schema import {model_name_pascal}Schema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

repo = Repo()  # Instantiate model repository class

# Create a new {nameSingular} instance.
@router.post("/", response_model=ModelSchema)
async def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return await repo.create(db=db, model_request=modelRequest)

# Retrieve a list of {namePlural}.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single {nameSingular} by ID.
@router.get("/{{model_id}}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{nameSingular} not found")
    return result

# Update an existing {nameSingular} by ID.
@router.put("/{{model_id}}", response_model=ModelSchema)
async def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{nameSingular} not found")
    return await repo.update(db=db, model_id=model_id, model_request=modelRequest)

# Retrieve counts or statistics related to {namePlural}.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a {nameSingular} by ID.
@router.put("/{{model_id}}/status/{{status_id}}")
async def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{nameSingular} not found")
    return await repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple {namePlural}.
@router.put("/statuses")
async def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = await repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{nameSingular} not found")
    return result

# Delete a {nameSingular} by ID.
@router.delete("/{{model_id}}")
async def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"{nameSingular} not found")
    return await repo.delete(db=db, model_id=model_id)
"""

    path = api_endpoint.replace('-', '_')
    filename = f'{nameSingular.lower()}_routes.py'
    handler(path, 'modules', filename, content)
