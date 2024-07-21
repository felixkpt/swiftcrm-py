from typing import Optional
from pydantic import BaseModel, Field

class ModelFieldSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=255)
    label: str = Field(..., max_length=255)
    dataType: str = Field(..., max_length=255)
    defaultValue: Optional[str] = Field(None, max_length=255)
    isVisibleInList: Optional[bool] = Field(None, max_length=None)
    isVisibleInSingleView: Optional[bool] = Field(None, max_length=None)
    isRequired: bool = Field(..., max_length=None)
    isUnique: Optional[bool] = Field(None, max_length=None)
    dropdownSource: Optional[str] = Field(None, max_length=255)
    dropdownDependsOn: Optional[str] = Field(None, max_length=None)
    desktopWidth: Optional[str] = Field(None, max_length=255)
    mobileWidth: Optional[str] = Field(None, max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
