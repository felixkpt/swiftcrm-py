from pydantic import BaseModel, Field

class QuestionSchema(BaseModel):
    category_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)
    question: str = Field(..., max_length=None)
    marks: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
