# app/routes/category.py
from fastapi import APIRouter, HTTPException
from app.requests.schemas.conversation.v1.category import CategoryRequest
from app.repositories.conversation.v1.category import CategoryRepo as Repo

from app.services.helpers import format_error


router = APIRouter()


@router.get("/categories")
async def categories():
    cats = Repo.get_cats()
    return cats


@router.get("/categories/{cat_id}")
async def get_category(cat_id: str):
    cat = Repo.get_cat(cat_id)
    return cat


@router.post("/categories")
async def create_category(category: CategoryRequest):
    if Repo.category_exists(category.name):
        raise HTTPException(status_code=400, detail=format_error(
            "name", "Category already exists."))
    try:
        Repo.add_category(category.name, category.description)
        return {"message": "Category added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add category: {e}")


@router.put("/categories/{category_id}")
async def update_category_endpoint(category_id: int, category: CategoryRequest):
    existing_category = Repo.get_cat(category_id)
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    try:
        Repo.update_category(category_id, category)
        return {"message": "Category updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update category: {e}")
