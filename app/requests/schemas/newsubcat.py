from pydantic import BaseModel, Field

class NewsubcatSchema(BaseModel):
    name: str = Field(..., max_length=255)
    description: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
