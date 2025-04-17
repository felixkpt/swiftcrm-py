from typing import Optional
from pydantic import BaseModel, Field

class ProjectSchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=None)
    skill_id: int = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
