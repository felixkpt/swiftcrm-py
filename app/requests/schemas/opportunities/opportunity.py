from pydantic import BaseModel, Field

class OpportunitySchema(BaseModel):
    name: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
