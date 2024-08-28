from typing import Optional
from pydantic import BaseModel, Field

class CustomerSchema(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    alternate_number: str = Field(..., max_length=255)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
