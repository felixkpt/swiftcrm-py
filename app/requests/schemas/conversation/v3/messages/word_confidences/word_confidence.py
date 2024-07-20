from pydantic import BaseModel, Field

class WordConfidenceSchema(BaseModel):
    message_id: int = Field(..., max_length=None)
    word: str = Field(..., max_length=255)
    start_time_seconds: int = Field(..., max_length=None)
    end_time_seconds: int = Field(..., max_length=None)
    confidence: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
