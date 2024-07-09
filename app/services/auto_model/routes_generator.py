from app.services.helpers import get_model_names
from app.services.auto_model.saves_file import handler
from app.services.str import STR


def generate_routes(api_endpoint, model_name):
    api_endpoint_slugged = api_endpoint.replace('/', '.').replace('-', '_')

    model_name_singular, model_name_plural, model_name_pascal = get_model_names(
        model_name)

    content = f"""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repositories.{api_endpoint_slugged+'.'+model_name_singular.lower()}_repo import {model_name_pascal}Repo as Repo
from app.requests.schemas.{api_endpoint_slugged+'.'+model_name_singular.lower()} import {model_name_pascal}Schema as ModelSchema
from app.requests.schemas.query_params import QueryParams
from app.database.connection import get_db

router = APIRouter()

@router.post("/", response_model=ModelSchema)
def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):
    return Repo.create(db=db, model_request=modelRequest)

@router.get("/")
def list_route(query_params: QueryParams = Depends(QueryParams), db: Session = Depends(get_db)):
    results = Repo.list(db, query_params)
    return results

@router.get("/{{model_id}}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name_singular} not found")
    return result

@router.put("/{{model_id}}", response_model=ModelSchema)
def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name_singular} not found")
    return Repo.update(db=db, model_id=model_id, model_request=modelRequest)

@router.delete("/{{model_id}}")
def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = Repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail="{model_name_singular} not found")
    return Repo.delete(db=db, model_id=model_id)
"""

    filename = f'{model_name_plural.lower()}.py'
    handler(api_endpoint, 'routes', filename, content)
