from typing import Optional
from pydantic import BaseModel, Field

class StringSchema(BaseModel):
    string: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
