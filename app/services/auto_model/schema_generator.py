# app/services/auto_model/schema_generator.py
import os
from app.services.helpers import get_model_names

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_schema(model_name, fields):
    model_name_singular, model_name_plural, model_name_pascal = get_model_names(model_name)

    # Dictionary to map field data types to Pydantic types
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'longtext': 'str',
    }

    content = f"""from pydantic import BaseModel

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

    directory_path = os.path.join(os.getcwd(), 'app', 'requests', 'schemas')
    create_directory_if_not_exists(directory_path)
    with open(os.path.join(directory_path, f'{model_name_singular.lower()}.py'), 'w') as f:
        f.write(content)
