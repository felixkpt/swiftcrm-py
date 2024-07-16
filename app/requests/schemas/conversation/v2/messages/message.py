from pydantic import BaseModel, Field

class MessageSchema(BaseModel):
    user_id: int = Field(..., max_length=None)
    category_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)
    role: str = Field(..., max_length=255)
    mode: str = Field(..., max_length=255)
    interview_id: int = Field(..., max_length=None)
    question_id: int = Field(..., max_length=None)
    question_scores: int = Field(..., max_length=None)
    content: str = Field(..., max_length=None)
    audio_uri: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
