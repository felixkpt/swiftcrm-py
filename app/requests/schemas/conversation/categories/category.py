from typing import Optional
from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
