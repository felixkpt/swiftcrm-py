from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from app.repositories.auto_page_builder_repo import AutoPageBuilderRepo as Repo
from app.services.auto_model.helpers import generate_model_and_api_names
from app.services.auto_model.auto_model_handler import auto_model_handler

router = APIRouter()

def prepare_data(auto_page_data):
    generated_data = generate_model_and_api_names(auto_page_data)
    auto_page_data.name_singular = generated_data['name_singular']
    auto_page_data.name_plural = generated_data['name_plural']
    auto_page_data.table_name_singular = generated_data['table_name_singular']
    auto_page_data.table_name_plural = generated_data['table_name_plural']
    auto_page_data.class_name = generated_data['class_name']
    return generated_data

@router.get("/auto-page-builder")
async def get_list_endpoint(db: Session = Depends(get_db)):
    return Repo.get_pages(db)

@router.get("/auto-page-builder/{page_id}")
async def get_page_endpoint(page_id: str, db: Session = Depends(get_db)):
    return Repo.get_page_by_id(db, page_id)

@router.post("/auto-page-builder")
async def store_endpoint(auto_page_data: AutoPageBuilderRequest, db: Session = Depends(get_db)):
    generated_data = prepare_data(auto_page_data)

    existing_page = Repo.get_page_by_name(db, generated_data['name_singular'])
    if existing_page:
        raise HTTPException(status_code=422, detail="A similar AutoPageBuilder configuration exists")

    try:
        auto_model_handler(generated_data, db)
        Repo.store_page(db, auto_page_data)
        return {"message": "AutoPageBuilder configuration stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store AutoPageBuilder configuration: {str(e)}")

@router.put("/auto-page-builder/{page_id}", response_model=dict)
async def update_endpoint(page_id: int, auto_page_data: AutoPageBuilderRequest, db: Session = Depends(get_db)):
    generated_data = prepare_data(auto_page_data)

    existing_page = Repo.get_page_by_id(db, page_id)
    if not existing_page:
        raise HTTPException(status_code=404, detail="AutoPageBuilder configuration not found")

    try:
        auto_model_handler(generated_data, db, page_id)
        Repo.update_page(db, page_id, auto_page_data)
        return {"message": "AutoPageBuilder configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update AutoPageBuilder configuration: {str(e)}")

@router.delete("/auto-page-builder/{page_id}", response_model=dict)
async def delete_endpoint(page_id: int, db: Session = Depends(get_db)):
    existing_page = Repo.get_page_by_id(db, page_id)
    if not existing_page:
        raise HTTPException(status_code=404, detail="AutoPageBuilder configuration not found")
    try:
        Repo.delete_page(db, page_id)
        return {"message": "AutoPageBuilder configuration deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete AutoPageBuilder configuration: {str(e)}")
