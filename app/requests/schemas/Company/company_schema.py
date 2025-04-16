from typing import Optional
from pydantic import BaseModel, Field

class CompanySchema(BaseModel):
    name: str = Field(..., max_length=255)
    address: str = Field(..., max_length=255)
    Number_of_employees: int = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
