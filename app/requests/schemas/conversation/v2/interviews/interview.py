from pydantic import BaseModel, Field

class InterviewSchema(BaseModel):
    user_id: int = Field(..., max_length=None)
    category_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)
    question_id: int = Field(..., max_length=None)
    scores: int = Field(..., max_length=None)
    max_scores: int = Field(..., max_length=None)
    percentage_score: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
