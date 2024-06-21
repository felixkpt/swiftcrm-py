import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_model_table(model_name, fields):
    model_name = model_name.capitalize()
    
    # Updated dictionary to map field data types to SQLAlchemy types
    type_mapping = {
        'string': {'name': 'String', 'length': 255},
        'integer': {'name': 'Integer', 'length': None},
        'longtext': {'name': 'Text', 'length': None},
    }
    
    # Collect the required imports based on fields
    imports = set()
    for field in fields:
        data_type = field.dataType.lower() if field.dataType else ''
        if data_type in type_mapping:
            imports.add(type_mapping[data_type]['name'])
        else:
            # Default to 'String' if data_type is invalid or None
            imports.add('String')
    
    # Create import statement dynamically
    imports_str = ', '.join(sorted(imports))
    import_statement = f"from sqlalchemy import Column, {imports_str}\n"
    
    # Base class import
    base_import = "from app.models.base import Base\n"
    
    # Start building the model class content
    content = f"{import_statement}{base_import}\n\nclass {model_name}(Base):\n    __tablename__ = '{model_name.lower()}'\n"
    
    for field in fields:
        data_type = field.dataType.lower() if field.dataType else ''
        sqlalchemy_type = type_mapping.get(data_type, {'name': 'String'})  # Default to 'String'
        column_type_name = sqlalchemy_type['name']
        column_args = f"({sqlalchemy_type['length']})" if sqlalchemy_type['length'] is not None else ''
        content += f"    {field.name} = Column({column_type_name}{column_args})\n"
    
    directory_path = os.path.join(os.getcwd(), 'app', 'models')
    create_directory_if_not_exists(directory_path)
    model_filename = f'{model_name.lower()}.py'
    model_filepath = os.path.join(directory_path, model_filename)
    
    with open(model_filepath, 'w') as f:
        f.write(content)
    
    # Update __init__.py to include import statement for the new model
    init_py_path = os.path.join(directory_path, '__init__.py')
    with open(init_py_path, 'a') as init_py:
        init_py.write(f"from .{model_filename[:-3]} import {model_name}\n")
