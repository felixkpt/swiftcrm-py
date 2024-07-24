from typing import Optional
from pydantic import BaseModel, Field

class ModelBuilder2Schema(BaseModel):
    uuid: str = Field(..., max_length=255)
    modelDisplayName: str = Field(..., max_length=255)
    name_singular: str = Field(..., max_length=255)
    name_plural: str = Field(..., max_length=255)
    modelURI: str = Field(..., max_length=255)
    apiEndpoint: str = Field(..., max_length=255)
    table_name_singular: str = Field(..., max_length=255)
    table_name_plural: str = Field(..., max_length=255)
    class_name: str = Field(..., max_length=255)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
