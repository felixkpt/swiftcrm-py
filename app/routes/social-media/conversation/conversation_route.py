from fastapi import APIRouter, HTTPException, Query, Depends, Request
from sqlalchemy.orm import Session
from app.repositories.social_media.conversation.conversation_repo import ConversationRepo as Repo
from app.repositories.social_media.conversation.messages.message_repo import MessageRepo
from app.repositories.social_media.conversation.database_seeder import seeder_handler_with_builder
from app.database.connection import get_db

router = APIRouter()

# Instantiate model repository classes
repo = Repo()
messageRepo = MessageRepo()


@router.get("/seeder")
async def set_database(db: Session = Depends(get_db)):
    res = await seeder_handler_with_builder(db)
    return {"message": res}


@router.get("/categories/{cat_id}/conversation")
async def cat_conversation(cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')"), db: Session = Depends(get_db)):
    conversation = messageRepo.get_cat_conversation(db, cat_id, mode=mode)
    return conversation


@router.get("/sub-categories/{sub_cat_id}/conversation")
async def sub_cat_conversation(request: Request, sub_cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')"), db: Session = Depends(get_db)):
    conversation = await messageRepo.get_sub_cat_conversation(db,
                                                        request, sub_cat_id, mode=mode)
    return conversation


@router.get("/reset-conversation")
async def reset_conversation(cat_id: str, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')")):
    repo.reset_messages(cat_id, mode=mode)
    return {"message": "Conversation reset."}


@router.put("/categories/{cat_id}/sub-categories/{sub_cat_id}/archive")
async def archive_conversation(cat_id: int, sub_cat_id: int, mode: str = Query(..., description="Mode type (e.g., 'training', 'interview')")):
    try:
        repo.archive_messages(cat_id, sub_cat_id, mode=mode)
        return {"message": "Conversation archived successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to archive conversation: {e}")
