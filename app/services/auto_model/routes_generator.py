import os
from app.services.helpers import get_model_names

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_routes(model_name, api_endpoint):
    model_name_singular, model_name_plural, model_name_pascal = get_model_names(model_name)


    content = f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories.{model_name_singular.lower()}_repo import {model_name_pascal}Repo as Repo
from app.requests.schemas.{model_name_singular.lower()} import {model_name_pascal}Schema as ModelSchema
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return Repo.create(db=db, model_request=modelRequest)

@router.get("/")
def list_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    results = Repo.list(db, skip=skip, limit=limit)
    return results

@router.get("/{{model_id}}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return result

@router.put("/{{model_id}}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return Repo.update(db=db, model_id=model_id, model_request=modelRequest)

@router.delete("/{{model_id}}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return Repo.delete(db=db, model_id=model_id)
"""

    # Determine the directory path based on api_endpoint
    directory_path = os.path.join(
        os.getcwd(), 'app', 'routes', *api_endpoint.split('/'))
    create_directory_if_not_exists(directory_path)

    # Create the route file
    route_filename = f'{model_name_plural.lower()}.py'
    route_file_path = os.path.join(directory_path, route_filename)

    with open(route_file_path, 'w') as f:
        f.write(content)
