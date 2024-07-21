from pydantic import BaseModel, Field

class ModelFieldSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    name: str = Field(..., max_length=255)
    type: str = Field(..., max_length=255)
    label: str = Field(..., max_length=255)
    dataType: str = Field(..., max_length=255)
    defaultValue: str = Field(..., max_length=255)
    dropdownSource: str = Field(..., max_length=255)
    isVisibleInList: str = Field(..., max_length=None)
    isVisibleInSingleView: str = Field(..., max_length=None)
    isRequired: str = Field(..., max_length=None)
    isUnique: str = Field(..., max_length=None)
    dropdownDependsOn: str = Field(..., max_length=None)
    desktopWidth: str = Field(..., max_length=255)
    mobileWidth: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
