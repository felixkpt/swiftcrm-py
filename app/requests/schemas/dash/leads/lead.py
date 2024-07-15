from pydantic import BaseModel, Field

class LeadSchema(BaseModel):
    dash_leads_categories_lead_category_id: int = Field(..., max_length=None)
    comments: str = Field(..., max_length=None)

    class Config:
        from_attributes = True
