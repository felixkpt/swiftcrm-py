from pydantic import BaseModel

class TicketSchema(BaseModel):
    source_id: int
    customer_id: int
    disposition_id: int

    class Config:
        from_attributes = True
