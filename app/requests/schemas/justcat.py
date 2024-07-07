from pydantic import BaseModel

class JustcatSchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
