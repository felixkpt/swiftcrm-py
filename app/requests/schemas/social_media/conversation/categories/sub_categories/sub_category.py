from typing import Optional
from pydantic import BaseModel, Field

class SubCategorySchema(BaseModel):
    name: str = Field(..., max_length=255)
    sub_category_id: int = Field(..., max_length=None)
    learn_instructions: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
