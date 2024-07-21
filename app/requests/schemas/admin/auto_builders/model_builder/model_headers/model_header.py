from pydantic import BaseModel, Field

class ModelHeaderSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    key: str = Field(..., max_length=255)
    label: str = Field(..., max_length=255)
    isVisibleInList: bool = Field(..., max_length=None)
    isVisibleInSingleView: bool = Field(..., max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
