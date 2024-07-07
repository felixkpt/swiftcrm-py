from fastapi import APIRouter, Query
from app.repositories.interviews import InterviewRepo as Repo
from typing import Dict, Any, Optional

router = APIRouter()


@router.get("/dashboard/interview/completed-by-categories")
async def route_list_completed_interviews():
    return Repo.list_completed_interviews_grouped_by_category()


@router.get("/dashboard/interview/completed-by-categories/{cat_id}")
async def route_list_completed_interviews(cat_id: str):
    return Repo.list_completed_interviews_grouped_by_sub_categories(cat_id)


@router.get("/dashboard/interview/{sub_cat_id}/progress")
async def get_interview_session_progress(sub_cat_id: str, interview_id: str = Query(..., description="Interview Session ID.")):
    progress = Repo.get_interview_progress(sub_cat_id, interview_id)
    return progress


@router.get("/dashboard/interview/results/categories", response_model=Dict[str, Any])
async def route_list_interviews_by_categories():
    return Repo.list_all_interviews()


@router.get("/dashboard/interview/results/categories/{category_id}", response_model=Dict[str, Any])
async def route_list_interviews_by_category_id(category_id: int):
    return Repo.list_interviews_by_category_id(category_id)


@router.get("/dashboard/interview/results/categories/{category_id}/sub-category/{sub_category_id}", response_model=Dict[str, Any])
async def route_list_interviews_by_category_sub_category_id(
    category_id: int,
    sub_category_id: int,
    status_id: Optional[int] = Query(default=None)
):
    return Repo.list_interviews_by_category_sub_category_id(category_id, sub_category_id, status_id)


@router.get("/dashboard/interview/results/{interview_id}")
async def get_interview_session_results(interview_id: str):
    results = Repo.get_interview_results(interview_id)
    return results
