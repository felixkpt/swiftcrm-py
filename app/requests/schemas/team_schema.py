from typing import Optional
from pydantic import BaseModel, Field

class TeamSchema(BaseModel):
    name: str = Field(..., max_length=255)
    number_of_members: int = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
