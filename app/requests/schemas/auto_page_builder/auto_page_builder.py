from typing import List, Optional, Any
from pydantic import BaseModel


class FieldSchema(BaseModel):
    name: str
    type: str
    label: str
    dataType: Optional[str] = None
    defaultValue: Optional[Any] = None
    isRequired: Optional[bool] = False
    isVisibleInList: Optional[bool] = False
    isVisibleInSingleView: Optional[bool] = False
    isUnique: Optional[bool] = False
    dropdownSource: Optional[str] = None
    dropdownDependsOn: Optional[List] = None
    desktopWidth: Optional[int] = 12  # Default desktop width
    mobileWidth: Optional[int] = 12    # Default mobile width


class ActionLabelSchema(BaseModel):
    key: str
    label: str
    actionType: str


class HeaderSchema(BaseModel):
    key: str
    label: str
    isVisibleInList: bool
    isVisibleInSingleView: bool


class AutoPageBuilderRequest(BaseModel):
    modelName: str
    name_singular: Optional[str] = None
    name_plural: Optional[str] = None
    modelURI: str
    apiEndpoint: str
    table_name_singular: Optional[str] = None
    table_name_plural: Optional[str] = None
    class_name: Optional[str] = None
    fields: List[FieldSchema]
    actionLabels: List[ActionLabelSchema]
    headers: List[HeaderSchema]

    class Config:
        from_attributes = True
