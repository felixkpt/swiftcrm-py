from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from app.repositories.auto_page_builder_repo import AutoPageBuilderRepo as repo

from app.services.auto_model.auto_model_handler import auto_model_handler

router = APIRouter()

# Endpoint to retrieve a list of AutoPageBuilders


@router.get("/dashboard/auto-page-builder")
async def get_list_endpoint(db: Session = Depends(get_db)):
    return repo.get_pages(db)


@router.get("/dashboard/auto-page-builder/{page_id}")
async def get_page_endpoint(page_id: str, db: Session = Depends(get_db)):
    return repo.get_page_by_id(db, page_id)

# Endpoint to store a new AutoPageBuilder configuration


@router.post("/dashboard/auto-page-builder")
async def store_endpoint(auto_page_data: AutoPageBuilderRequest, db: Session = Depends(get_db)):
    existing_page = repo.get_page_by_name(db, 'dfdfdfdff'+auto_page_data.modelName)
    if existing_page:
        raise HTTPException(
            status_code=422, detail="A similar AutoPageBuilder configuration exists")
    # try:
    auto_model_handler(auto_page_data)
    repo.store_page(db, auto_page_data)
    return {"message": "AutoPageBuilder configuration stored successfully"}
    # except Exception as e:
    #     print('e::',e)
    #     raise HTTPException(
    #         status_code=500, detail=f"Failed to store AutoPageBuilder configuration: {str(e)}")

# Endpoint to update an existing AutoPageBuilder configuration


@router.put("/dashboard/auto-page-builder/{page_id}", response_model=dict)
async def update_endpoint(page_id: int, auto_page_data: AutoPageBuilderRequest, db: Session = Depends(get_db)):
    existing_page = repo.get_page_by_id(db, page_id)
    if not existing_page:
        raise HTTPException(
            status_code=404, detail="AutoPageBuilder configuration not found")
    try:
        repo.update_page(db, page_id, auto_page_data)
        return {"message": "AutoPageBuilder configuration updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update AutoPageBuilder configuration: {str(e)}")

# Endpoint to delete an existing AutoPageBuilder configuration


@router.delete("/dashboard/auto-page-builder/{page_id}", response_model=dict)
async def delete_endpoint(page_id: int, db: Session = Depends(get_db)):
    existing_page = repo.get_page_by_id(db, page_id)
    if not existing_page:
        raise HTTPException(
            status_code=404, detail="AutoPageBuilder configuration not found")
    try:
        repo.delete_page(db, page_id)
        return {"message": "AutoPageBuilder configuration deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete AutoPageBuilder configuration: {str(e)}")
