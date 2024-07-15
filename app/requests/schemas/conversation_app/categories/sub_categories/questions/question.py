from pydantic import BaseModel, Field

class QuestionSchema(BaseModel):
    conversation_app_category_id: int = Field(..., max_length=None)
    conversation_app_categories_sub_category_id: int = Field(..., max_length=None)
    question: str = Field(..., max_length=255)
    marks: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
