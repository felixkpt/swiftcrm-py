from pydantic import BaseModel

class SysOpportunitySchema(BaseModel):
    source_id: str

    class Config:
        from_attributes = True
