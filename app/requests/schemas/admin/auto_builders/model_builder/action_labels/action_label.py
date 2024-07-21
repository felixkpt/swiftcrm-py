from pydantic import BaseModel, Field

class ActionLabelSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    key: str = Field(..., max_length=255)
    label: str = Field(..., max_length=255)
    actionType: str = Field(..., max_length=255)
    show: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
