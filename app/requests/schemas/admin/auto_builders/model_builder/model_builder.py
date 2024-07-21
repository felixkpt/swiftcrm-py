from pydantic import BaseModel, Field

class ModelBuilderSchema(BaseModel):
    name_singular: str = Field(..., max_length=255)
    name_plural: str = Field(..., max_length=255)
    modelURI: str = Field(..., max_length=255)
    apiEndpoint: str = Field(..., max_length=255)
    table_name_singular: str = Field(..., max_length=255)
    table_name_plural: str = Field(..., max_length=255)
    class_name: str = Field(..., max_length=255)

    class Config:
        from_attributes = True
        protected_namespaces = ()
