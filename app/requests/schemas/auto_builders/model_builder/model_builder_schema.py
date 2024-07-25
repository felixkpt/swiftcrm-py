from typing import Optional
from pydantic import BaseModel, Field

class ModelBuilderSchema(BaseModel):
    uuid: Optional[str] = Field(None, max_length=255)
    modelDisplayName: str = Field(..., max_length=255)
    name_singular: Optional[str] = Field(None, max_length=255)
    name_plural: Optional[str] = Field(None, max_length=255)
    modelURI: str = Field(..., max_length=255)
    apiEndpoint: str = Field(..., max_length=255)
    table_name_singular: Optional[str] = Field(None, max_length=255)
    table_name_plural: Optional[str] = Field(None, max_length=255)
    class_name: Optional[str] = Field(None, max_length=255)
    createFrontendViews: bool = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
