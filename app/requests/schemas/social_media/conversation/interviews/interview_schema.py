from typing import Optional
from pydantic import BaseModel, Field

class InterviewSchema(BaseModel):
    category_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)
    current_question_id: int = Field(..., max_length=None)
    scores: int = Field(..., max_length=None)
    max_scores: int = Field(..., max_length=None)
    percentage_score: int = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
