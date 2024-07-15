from pydantic import BaseModel, Field

class SubCategorySchema(BaseModel):
    conversation_app_category_id: int = Field(..., max_length=None)
    name: str = Field(..., max_length=255)
    learn_instructions: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
