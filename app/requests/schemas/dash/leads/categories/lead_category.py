from pydantic import BaseModel, Field

class LeadCategorySchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
