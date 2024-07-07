from pydantic import BaseModel

class Categories2Schema(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True
