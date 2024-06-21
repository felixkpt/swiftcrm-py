# app/services/auto_model/routes_generator.py
import os
import importlib.util

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_routes(model_name):
    model_name = model_name.capitalize()
    content = f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.crud import {model_name.lower()} as crud
from app.requests.schemas import {model_name.lower()} as schema
from app.database.connection import get_db

router = APIRouter()

@router.post("/{model_name.lower()}/", response_model=schema.{model_name}Schema)
def create_{model_name.lower()}({model_name.lower()}: schema.{model_name}Schema, db: Session = Depends(get_db)):
    return crud.create_{model_name.lower()}(db=db, {model_name.lower()}={model_name.lower()})

@router.get("/{model_name.lower()}/{{{model_name.lower()}_id}}", response_model=schema.{model_name}Schema)
def read_{model_name.lower()}({model_name.lower()}_id: int, db: Session = Depends(get_db)):
    db_{model_name.lower()} = crud.get_{model_name.lower()}(db, {model_name.lower()}_id={model_name.lower()}_id)
    if db_{model_name.lower()} is None:
        raise HTTPException(status_code=404, detail="{model_name} not found")
    return db_{model_name.lower()}

@router.get("/{model_name.lower()}/", response_model=list[schema.{model_name}Schema])
def read_{model_name.lower()}(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    {model_name.lower()} = crud.get_{model_name.lower()}(db, skip=skip, limit=limit)
    return {model_name.lower()}
"""

    directory_path = os.path.join(os.getcwd(), 'app', 'routes')
    create_directory_if_not_exists(directory_path)
    route_filename = f'{model_name.lower()}.py'
    route_file_path = os.path.join(directory_path, route_filename)
    
    with open(route_file_path, 'w') as f:
        f.write(content)

    # Dynamically import the route module into main.py
    module_name = route_filename[:-3]  # Remove '.py' extension
    spec = importlib.util.spec_from_file_location(module_name, route_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.router
