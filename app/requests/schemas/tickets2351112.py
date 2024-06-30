from pydantic import BaseModel

class Tickets2351112Schema(BaseModel):
    source_id: str

    class Config:
        from_attributes = True
