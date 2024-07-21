from typing import Optional
from pydantic import BaseModel, Field

class SubCategorySchema(BaseModel):
    name: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
