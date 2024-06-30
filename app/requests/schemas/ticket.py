from pydantic import BaseModel

class TicketSchema(BaseModel):
    source_id: str

    class Config:
        from_attributes = True
