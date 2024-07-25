from typing import List, Optional
from app.requests.schemas.auto_builders.model_builder.model_builder import ModelBuilderSchema
from app.requests.schemas.auto_builders.model_builder.model_headers.model_header import ModelHeaderSchema
from app.requests.schemas.auto_builders.model_builder.model_fields.model_field import ModelFieldSchema
from app.requests.schemas.auto_builders.model_builder.action_labels.action_label import ActionLabelSchema

class ModelHeaderSchemaWithoutID(ModelHeaderSchema):
    model_builder_id: Optional[int] = None

class ModelFieldSchemaWithoutID(ModelFieldSchema):
    model_builder_id: Optional[int] = None

class ActionLabelSchemaWithoutID(ActionLabelSchema):
    model_builder_id: Optional[int] = None

class ModelBuilderRequest(ModelBuilderSchema):
    headers: List[ModelHeaderSchemaWithoutID]
    fields: List[ModelFieldSchemaWithoutID]
    actionLabels: List[ActionLabelSchemaWithoutID]

    class Config:
        from_attributes = True
