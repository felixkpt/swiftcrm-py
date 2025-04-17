from typing import Optional
from pydantic import BaseModel, Field

class NovelSchema(BaseModel):
    name: str = Field(..., max_length=255)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
