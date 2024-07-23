from typing import Optional
from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    user_id: Optional[str] = Field(None, max_length=255)
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
