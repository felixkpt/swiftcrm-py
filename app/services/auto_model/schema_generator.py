# app/services/auto_model/schema_generator.py
from app.services.auto_model.saves_file import handler

def generate_schema(data):
    api_endpoint = data['api_endpoint']
    fields = data['fields']
    model_name_pascal = data['model_name_pascal']
    model_name_singular = data['model_name_singular']

    # Dictionary to map field data types to Pydantic types
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'longtext': 'str',
    }

    content = f"""from pydantic import BaseModel, Field\n
class {model_name_pascal}Schema(BaseModel):
"""
    for field in fields:
        if field.name in ['id', 'created_at', 'updated_at']:
            continue  # Skip id, created_at, and updated_at fields
        # Determine Pydantic type and add Field constraints
        pydantic_type = type_mapping.get(field.dataType, 'str')
        max_length = 255 if field.dataType == 'string' else None
        content += f"    {field.name}: {pydantic_type} = Field(..., max_length={max_length})\n"

    content += """
    class Config:
        from_attributes = True
"""

    path = api_endpoint.replace('-', '_')
    filename = f'{model_name_singular.lower()}.py'
    handler(path, 'requests/schemas', filename, content)