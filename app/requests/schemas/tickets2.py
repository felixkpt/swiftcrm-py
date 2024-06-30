from pydantic import BaseModel

class Tickets2Schema(BaseModel):
    source_id: str

    class Config:
        from_attributes = True
