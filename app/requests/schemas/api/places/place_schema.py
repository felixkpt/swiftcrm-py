from typing import Optional
from pydantic import BaseModel, Field

class PlaceSchema(BaseModel):
    name: str = Field(..., max_length=255)
    address: str = Field(..., max_length=255)
    featured_image: str = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
