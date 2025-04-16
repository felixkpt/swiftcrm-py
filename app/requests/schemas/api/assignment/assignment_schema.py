from typing import Optional
from pydantic import BaseModel, Field

class AssignmentSchema(BaseModel):
    name: str = Field(..., max_length=255)
    lecturer: str = Field(..., max_length=255)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
