from typing import List, Optional
from app.modules.auto_builders.model_builder.model_builder_schema import ModelBuilderSchema
from app.modules.auto_builders.model_builder.model_headers.model_header_schema import ModelHeaderSchema
from app.modules.auto_builders.model_builder.model_fields.model_field_schema import ModelFieldSchema
from app.modules.auto_builders.model_builder.action_labels.action_label_schema import ActionLabelSchema

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
