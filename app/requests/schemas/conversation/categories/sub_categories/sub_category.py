from typing import Optional
from pydantic import BaseModel, Field

class SubCategorySchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    sub_category_id: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
