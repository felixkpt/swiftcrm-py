from app.modules.auto_builders.model_builder.services.saves_file import handler

def generate_schema(data):
    api_endpoint = data['api_endpoint']
    fields = data['fields']
    model_name_pascal = data['model_name_pascal']
    nameSingular = data['nameSingular']

    # Dictionary to map field data types to Pydantic types
    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'boolean': 'bool',
        'longtext': 'str',
    }

    content = f"""from typing import Optional\nfrom pydantic import BaseModel, Field\n\nclass {model_name_pascal}Schema(BaseModel):\n"""
    
    for field in fields:
        if field['name'] in ['id', 'created_at', 'updated_at']:
            continue  # Skip id, created_at, and updated_at fields
        
        # Determine Pydantic type and add Field constraints
        pydantic_type = type_mapping.get(field['dataType'], 'str')
        max_length = 255 if field['dataType'] == 'string' else None

        # Determine if the field is required or optional
        if field.get('isRequired', False):
            content += f"    {field['name']}: {pydantic_type} = Field(..., max_length={max_length})\n"
        else:
            content += f"    {field['name']}: Optional[{pydantic_type}] = Field(None, max_length={max_length})\n"

    content += """
    class Config:
        from_attributes = True
        protected_namespaces = ()
"""

    path = api_endpoint.replace('-', '_')
    filename = f'{nameSingular.lower()}_schema.py'
    handler(path, 'modules', filename, content)
