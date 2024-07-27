from typing import Optional
from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    category_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)
    role: str = Field(..., max_length=255)
    mode: str = Field(..., max_length=255)
    content: str = Field(..., max_length=None)
    interview_id: int = Field(..., max_length=None)
    question_id: int = Field(..., max_length=None)
    question_scores: int = Field(..., max_length=None)
    audio_uri: int = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
