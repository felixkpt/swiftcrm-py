from pydantic import BaseModel, Field
from typing import Optional

class SubCategoryRequest(BaseModel):
    name: str = Field(..., max_length=255)
    slug: str | None
    learn_instructions: Optional[str]

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    marks: int = Field(..., ge=1, le=5)
