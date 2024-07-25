from typing import Optional
from pydantic import BaseModel, Field

class ActionLabelSchema(BaseModel):
    model_builder_id: int = Field(..., max_length=None)
    key: str = Field(..., max_length=255)
    label: Optional[str] = Field(None, max_length=255)
    actionType: str = Field(..., max_length=255)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
