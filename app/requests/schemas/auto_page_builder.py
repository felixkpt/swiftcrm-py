from typing import List, Optional, Any
from pydantic import BaseModel


class FieldSchema(BaseModel):
    name: str
    type: str
    label: str
    isRequired: bool
    dataType: Optional[str] = None
    defaultValue: Optional[Any] = None
    dropdownSource: Optional[str] = None
    dropdownDependsOn: Optional[List] = None


class ActionLabelSchema(BaseModel):
    key: str
    label: str
    actionType: str
    show: bool
    required: bool
    isRequired: bool


class HeaderSchema(BaseModel):
    key: str
    label: str
    isVisibleInList: bool
    isVisibleInSingleView: bool


class AutoPageBuilderRequest(BaseModel):
    modelName: str
    modelURI: str
    apiEndpoint: str
    fields: List[FieldSchema]
    actionLabels: List[ActionLabelSchema]
    headers: List[HeaderSchema]

    class Config:
        from_attributes = True
