from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.repositories.conversation.v1.conversation_repo import ConversationRepo as Repo
from app.repositories.conversation.v2.categories.category_repo import CategoryRepo as catsRepo
from app.repositories.conversation.v2.messages.message_repo import MessageRepo
from app.repositories.conversation.v2.database_seeder import seeder_handler
from app.database.connection import get_db

router = APIRouter()


@router.get("/seeder")
async def set_database(db: Session = Depends(get_db)):
    res = seeder_handler(db)
    return {"message": res}


@router.get("/categories/{cat_id}/conversation")
async def cat_conversation(cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')"), db: Session = Depends(get_db)):
    conversation = MessageRepo.get_cat_conversation(db, cat_id, mode=mode)
    return conversation


@router.get("/sub-categories/{sub_cat_id}/conversation")
async def sub_cat_conversation(sub_cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')"), interview_id: str = Query(None, description="Interview Session ID."), db: Session = Depends(get_db)):
    conversation = MessageRepo.get_sub_cat_conversation(db, 
        sub_cat_id, mode=mode, interview_id=interview_id)
    return conversation


@router.get("/reset-conversation")
async def reset_conversation(cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')")):
    Repo.reset_messages(cat_id, mode=mode)
    return {"message": "Conversation reset."}


@router.put("/categories/{cat_id}/sub-categories/{sub_cat_id}/archive")
async def archive_conversation(cat_id: int, sub_cat_id: int, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')")):
    try:
        Repo.archive_messages(cat_id, sub_cat_id, mode=mode)
        return {"message": "Conversation archived successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to archive conversation: {e}")
