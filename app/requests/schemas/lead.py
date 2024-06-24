from pydantic import BaseModel

class LeadSchema(BaseModel):
    source_id: int
    customer_id: int
    category_id: int
    sub_category_id: int
    disposition_id: int
    comments: str

    class Config:
        from_attributes = True
