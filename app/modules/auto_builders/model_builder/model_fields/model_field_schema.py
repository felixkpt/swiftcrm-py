from typing import Optional, List
from pydantic import BaseModel, Field

class ModelFieldSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=255)
    label: Optional[str] = Field(None, max_length=255)
    dataType: str = Field(..., max_length=255)
    defaultValue: Optional[str] = Field(None, max_length=255)
    isVisibleInList: bool = Field(..., max_length=None)
    isVisibleInSingleView: bool = Field(..., max_length=None)
    isRequired: Optional[bool] = Field(None, max_length=None)
    isUnique: Optional[bool] = Field(None, max_length=None)
    dropdownSource: Optional[str] = Field(None, max_length=255)
    dropdownDependsOn: Optional[List] = Field(None, max_length=None)
    desktopWidth: Optional[int] = Field(None, max_length=None)
    mobileWidth: Optional[int] = Field(None, max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
