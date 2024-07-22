from typing import Optional
from pydantic import BaseModel, Field

class ModelBuilderSchema(BaseModel):
    uuid: str = Field(..., max_length=255)
    modelDisplayName: str = Field(..., max_length=255)
    name_singular: Optional[str] = Field(None, max_length=255)
    name_plural: Optional[str] = Field(None, max_length=255)
    modelURI: str = Field(..., max_length=255)
    apiEndpoint: str = Field(..., max_length=255)
    table_name_singular: Optional[str] = Field(None, max_length=255)
    table_name_plural: Optional[str] = Field(None, max_length=255)
    class_name: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
