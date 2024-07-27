from typing import Optional
from pydantic import BaseModel, Field

class WordConfidenceSchema(BaseModel):
    message_id: int = Field(..., max_length=None)
    word: str = Field(..., max_length=255)
    start_time_seconds: int = Field(..., max_length=None)
    start_time_nanos: str = Field(..., max_length=255)
    end_time_seconds: int = Field(..., max_length=None)
    end_time_nanos: int = Field(..., max_length=None)
    confidence: str = Field(..., max_length=None)
    user_id: Optional[int] = Field(None, max_length=None)

    class Config:
        from_attributes = True
        protected_namespaces = ()
