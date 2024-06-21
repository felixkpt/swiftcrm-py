# app/routes/auto_page_builder.py
# Import necessary modules
from fastapi import APIRouter, HTTPException
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from app.database.crud.auto_page_builder import get_pages, store_page, update_page, delete_page, get_page_by_id, get_page_by_name
from app.services.auto_model.generate_model import auto_model_handler

# Create a router instance
router = APIRouter()

# Endpoint to retrieve a list of AutoPageBuilders


@router.get("/dashboard/auto-page-builder")
async def get_list_endpoint():
    return get_pages()

# Endpoint to store a new AutoPageBuilder configuration


@router.post("/dashboard/auto-page-builder")
async def store_endpoint(auto_page_data: AutoPageBuilderRequest):
    existing_page = get_page_by_name('ssdsdd'+auto_page_data.modelName)
    if existing_page:
        raise HTTPException(
            status_code=422, detail="A similar AutoPageBuilder configuration exists")
    try:
        store_page(auto_page_data)
        auto_model_handler(auto_page_data)
        return {"message": "AutoPageBuilder configuration stored successfully"}
    except Exception as e:
        print("Error!", e)
        raise HTTPException(
            status_code=500, detail=f"Failed to store AutoPageBuilder configuration: {e}")

# Endpoint to update an existing AutoPageBuilder configuration


@router.put("/dashboard/auto-page-builder/{page_id}")
async def update_endpoint(page_id: int, auto_page_data: AutoPageBuilderRequest):
    existing_page = get_page_by_id(page_id)
    if not existing_page:
        raise HTTPException(
            status_code=404, detail="AutoPageBuilder configuration not found")
    try:
        update_page(page_id, auto_page_data)
        return {"message": "AutoPageBuilder configuration updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update AutoPageBuilder configuration: {e}")

# Endpoint to delete an existing AutoPageBuilder configuration


@router.delete("/dashboard/auto-page-builder/{page_id}")
async def delete_endpoint(page_id: int):
    existing_page = get_page_by_id(page_id)
    if not existing_page:
        raise HTTPException(
            status_code=404, detail="AutoPageBuilder configuration not found")
    try:
        delete_page(page_id)
        return {"message": "AutoPageBuilder configuration deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete AutoPageBuilder configuration: {e}")