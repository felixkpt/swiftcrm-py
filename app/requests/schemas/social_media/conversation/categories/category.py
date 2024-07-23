from typing import Optional
from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=None)
    user_id: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
