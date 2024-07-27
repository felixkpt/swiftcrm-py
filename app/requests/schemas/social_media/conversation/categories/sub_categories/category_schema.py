from typing import Optional
from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    name: str = Field(..., max_length=255)
    category_id: int = Field(..., max_length=None)
    learn_instructions: str = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
