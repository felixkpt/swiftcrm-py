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
    modelURI: str
    apiEndpoint: str
    table_name: Optional[str] = None
    class_name: Optional[str] = None
    fields: List[FieldSchema]
    actionLabels: List[ActionLabelSchema]
    headers: List[HeaderSchema]

    class Config:
        from_attributes = True
