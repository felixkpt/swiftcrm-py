from pydantic import BaseModel

class TicketSchema(BaseModel):
    source_id: int
    comment: str

    class Config:
        from_attributes = True
