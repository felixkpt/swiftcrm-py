from pydantic import BaseModel, Field

class LeadSchema(BaseModel):
    name: str = Field(..., max_length=255)
    category_id: int = Field(..., max_length=None)

    class Config:
        from_attributes = True
