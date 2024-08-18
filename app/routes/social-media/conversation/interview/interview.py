from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy.orm import Session
from app.repositories.social_media.conversation.interviews.interview_repo_old import InterviewRepo as Repo
from typing import Dict, Any, Optional
from app.database.connection import get_db

router = APIRouter()


@router.get("/completed-by-categories")
async def route_list_completed_interviews():
    return Repo.list_completed_interviews_grouped_by_category()


@router.get("/completed-by-categories/{category_id}")
async def route_list_completed_interviews(category_id: str):
    return Repo.list_completed_interviews_grouped_by_sub_categories(category_id)


@router.get("/{sub_category_id}/progress")
async def get_interview_session_progress(request: Request, sub_category_id: str, db: Session = Depends(get_db)):
    progress = await Repo.get_interview_progress(
        db, request, sub_category_id)
    return progress


@router.get("/results/categories", response_model=Dict[str, Any])
async def route_list_interviews_by_categories():
    return Repo.list_all_interviews()


@router.get("/results/categories/{category_id}", response_model=Dict[str, Any])
async def route_list_interviews_by_category_id(category_id: int):
    return Repo.list_interviews_by_category_id(category_id)


@router.get("/results/categories/{category_id}/sub-category/{sub_category_id}", response_model=Dict[str, Any])
async def route_list_interviews_by_category_sub_category_id(
    category_id: int,
    sub_category_id: int,
    status_id: Optional[int] = Query(default=None)
):
    return Repo.list_interviews_by_category_sub_category_id(category_id, sub_category_id, status_id)


@router.get("/results/{interview_id}")
async def get_interview_session_results(interview_id: str):
    results = Repo.get_interview_results(interview_id)
    return results
