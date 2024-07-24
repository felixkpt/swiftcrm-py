from typing import Optional
from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    first_name: str = Field(..., max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    email: str = Field(..., max_length=255)
    phone_number: str = Field(..., max_length=255)
    password: str = Field(..., max_length=None)
    password_confirmation: str = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
