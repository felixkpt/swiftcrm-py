# app/services/auto_model/schema_generator.py
import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_schema(model_name, fields):
    # Dictionary to map field data types to Pydantic types
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'longtext': 'str',
    }

    content = f"""from pydantic import BaseModel

class {model_name}Schema(BaseModel):
"""
    for field in fields:
        if field.name in ['id', 'created_at', 'updated_at']:
            continue  # Skip id, created_at, and updated_at fields
        # Get the appropriate Pydantic type or default to 'str'
        pydantic_type = type_mapping.get(
            field.dataType.lower(), 'str') if field.dataType else 'str'
        content += f"    {field.name}: {pydantic_type}\n"

    content += """
    class Config:
        from_attributes = True
"""

    directory_path = os.path.join(os.getcwd(), 'app', 'requests', 'schemas')
    create_directory_if_not_exists(directory_path)
    with open(os.path.join(directory_path, f'{model_name.lower()}.py'), 'w') as f:
        f.write(content)
