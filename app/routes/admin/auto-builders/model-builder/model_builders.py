
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.repositories.admin.auto_builders.model_builder.model_builder_repo import ModelBuilderRepo as Repo
from app.requests.schemas.admin.auto_builders.model_builder.model_builder_request import ModelBuilderRequest as ModelSchema
from app.database.connection import get_db
from app.events.notifications import NotificationService  # Import NotificationService
from app.services.auto_model.helpers import generate_model_and_api_names
from app.services.auto_model.auto_model_handler import auto_model_handler

router = APIRouter()

repo = Repo()  # Instantiate model repository class
notification = NotificationService() # Instantiate notification class

def prepare_data(model_request: ModelSchema):
    generated_data = generate_model_and_api_names(model_request)
    model_request.name_singular = generated_data['name_singular']
    model_request.name_plural = generated_data['name_plural']
    model_request.table_name_singular = generated_data['table_name_singular']
    model_request.table_name_plural = generated_data['table_name_plural']
    model_request.class_name = generated_data['class_name']
    return generated_data

# Create a new Model_builder instance.
@router.post("/", response_model=None)
async def create_route(modelRequest: ModelSchema, db: Session = Depends(get_db)):

    generated_data = prepare_data(modelRequest)
    existing_page = Repo.get_page_by_table_name(db, generated_data['table_name_singular'])
    if existing_page:
        raise HTTPException(status_code=422, detail="A similar AutoPageBuilder configuration exists")

    try:
        auto_model_handler(generated_data, db)
        modelRequest.table_name_singular = generated_data['table_name_singular']
        modelRequest.table_name_plural = generated_data['table_name_plural']
        await repo.create(db=db, model_request=modelRequest)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store AutoPageBuilder configuration: {str(e)}")


# Retrieve a list of Model_builders.
@router.get("/")
async def list_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results

# Retrieve a single Model_builder by ID.
@router.get("/{model_id}")
def view_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Model_builder not found")
    return result

# Update an existing Model_builder by ID.
@router.put("/{model_id}", response_model=None)
async def update_route(model_id: int, modelRequest: ModelSchema, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Model_builder not found")
    
    generated_data = prepare_data(modelRequest)
    auto_model_handler(generated_data, db, model_id)
    return {}
    
    modelRequest.table_name_singular = generated_data['table_name_singular']
    modelRequest.table_name_plural = generated_data['table_name_plural']
    await repo.update(db=db, model_id=model_id, model_request=modelRequest)

    return {"message": "AutoPageBuilder configuration updated successfully"}

# Retrieve counts or statistics related to Model_builders.
@router.get("/counts")
async def counts_route(request: Request, db: Session = Depends(get_db)):
    results = await repo.list(db, request)
    return results.metadata.total_counts

# Update the status of a Model_builder by ID.
@router.put("/{model_id}/status/{status_id}")
async def update_status_route(model_id: int, status_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Model_builder not found")
    return await repo.update_status(db=db, model_id=model_id, status_id=status_id)

# Update statuses of multiple Model_builders.
@router.put("/statuses")
async def update_statuses_route(request: Request, status_id: int, db: Session = Depends(get_db)):
    result = await repo.update_multiple_statuses(db, request, status_id=status_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Model_builder not found")
    return result

# Delete a Model_builder by ID.
@router.delete("/{model_id}")
async def delete_route(model_id: int, db: Session = Depends(get_db)):
    result = repo.get(db, model_id=model_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Model_builder not found")
    return await repo.delete(db=db, model_id=model_id)
