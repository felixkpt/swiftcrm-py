from pydantic import BaseModel, Field

class CoreCategorySchema(BaseModel):
    user_id: int = Field(..., max_length=None)
    sub_category_id: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
