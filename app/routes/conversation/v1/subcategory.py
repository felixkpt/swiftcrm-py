from fastapi import APIRouter, HTTPException
from app.requests.schemas.conversation.v1.sub_category import SubCategoryRequest, QuestionRequest
from app.repositories.conversation.v1.sub_category import SubCategoryRepo as Repo

from app.services.helpers import format_error

router = APIRouter()


@router.get("/categories/{cat_id}/sub-categories")
async def sub_categories(cat_id: str):
    sub_cats = Repo.get_sub_cats(cat_id)
    return sub_cats


@router.get("/categories/{cat_id}/sub-categories/{sub_cat_id}")
async def get_sub_category(sub_cat_id: str):
    sub_cat = Repo.get_sub_cat(sub_cat_id)
    return sub_cat


@router.post("/categories/{cat_id}/sub-categories")
async def create_sub_category(cat_id: str, sub_category: SubCategoryRequest):
    if Repo.sub_category_exists(cat_id, sub_category.name):
        raise HTTPException(
            status_code=400, detail=format_error("name", "Sub-category already exists."))
    try:
        sub_cat_id = Repo.add_sub_category(
            cat_id, sub_category.name, sub_category.slug, sub_category.learn_instructions)
        return {"message": "Sub-category added successfully", "sub_category_id": sub_cat_id}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add sub-category: {e}")


@router.put("/categories/{cat_id}/sub-categories/{sub_cat_id}")
async def update_sub_category_endpoint(sub_cat_id: int, sub_category: SubCategoryRequest):
    existing_sub_category = Repo.get_sub_cat(sub_cat_id)
    if not existing_sub_category:
        raise HTTPException(status_code=404, detail=format_error(
            "name", "Sub-category not found"))
    try:
        Repo.update_sub_category(sub_cat_id, sub_category)
        return {"message": "Sub-category updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update sub-category: {e}")


@router.get("/categories/{cat_id}/sub-categories/{sub_cat_id}/questions")
async def get_sub_category_questions(sub_cat_id: str):
    sub_cats = Repo.get_sub_cat_questions(sub_cat_id)
    return sub_cats

@router.post("/categories/{cat_id}/sub-categories/{sub_cat_id}/questions")
async def add_question(cat_id: int, sub_cat_id: int, question: QuestionRequest):
    try:
        # Check if the category exists
        category = Repo.get_cat(cat_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # Check if the question already exists
        if Repo.question_exists(sub_cat_id, question.question):
            raise HTTPException(status_code=400, detail=format_error(
                "question", "Question already exists"))

        # Add questions to sub-category
        Repo.add_question_to_sub_category(sub_cat_id, question)
        return {"message": "Question added to sub-category successfully"}
    except HTTPException as http_ex:
        raise http_ex  # Re-raise HTTPException to maintain the response status and detail
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to add question: {e}")


@router.put("/categories/{cat_id}/sub-categories/{sub_cat_id}/questions/{question_id}")
async def update_quiz(question_id: int, question: QuestionRequest):
    existing_question = Repo.get_question(question_id)
    if not existing_question:
        raise HTTPException(status_code=404, detail=format_error(
            "question", "Question not found"))
    try:
        Repo.update_question(question_id, question)
        return {"message": "Question updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update question: {e}")
