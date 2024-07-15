from pydantic import BaseModel, Field

class TestrevalidateCatSchema(BaseModel):
    name: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
