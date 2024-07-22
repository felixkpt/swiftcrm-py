from typing import Optional
from pydantic import BaseModel, Field

class CustomerSchema(BaseModel):
    name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
