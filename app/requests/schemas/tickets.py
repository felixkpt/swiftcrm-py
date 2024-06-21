from pydantic import BaseModel

class TicketsSchema(BaseModel):
    string1: str
    string3: int

    class Config:
        from_attributes = True
