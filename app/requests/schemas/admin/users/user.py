from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    username: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    password: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
