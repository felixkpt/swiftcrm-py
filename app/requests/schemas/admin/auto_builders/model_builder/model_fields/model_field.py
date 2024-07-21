from typing import Optional
from pydantic import BaseModel, Field

class ModelFieldSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=255)
    label: str = Field(..., max_length=255)
    dataType: str = Field(..., max_length=255)
    defaultValue: Optional[str] = Field(None, max_length=255)
    isVisibleInList: bool = Field(..., max_length=None)
    isVisibleInSingleView: bool = Field(..., max_length=None)
    isRequired: bool = Field(..., max_length=None)
    isUnique: bool = Field(..., max_length=None)
    dropdownSource: Optional[str] = Field(None, max_length=255)
    dropdownDependsOn: Optional[str] = Field(None, max_length=None)
    desktopWidth: str = Field(..., max_length=255)
    mobileWidth: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
