# app/services/auto_model/model_generator.py
import os
import subprocess
from app.services.helpers import get_model_names

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_model(model_name, fields, options=None):

    model_name_singular, model_name_plural, model_name_pascal = get_model_names(model_name)

    # Updated dictionary to map field data types to SQLAlchemy types
    type_mapping = {
        'string': {'name': 'String', 'length': 255},
        'integer': {'name': 'Integer', 'length': None},
        'longtext': {'name': 'Text', 'length': None},
    }

# Check if 'id' field exists in fields
    id_field = next((field for field in fields if field['name'] == 'id'), None)

    if id_field is None:
        # If 'id' field does not exist, add it as the primary key and set auto-increments
        fields.insert(0, {
            "name": "id",
            "type": "integer",
            "label": "id",
            "dataType": "integer",
            "isPrimaryKey": True,
            "autoIncrements": True,
            "isRequired": False,
            "defaultValue": None,
            "hidden": True
        })
    else:
        # If 'id' field exists but not set as primary key and auto-increment, update it
        id_field.update({
            "dataType": id_field['dataType'] or 'integer',
            "isPrimaryKey": True,
            "autoIncrements": True
        })

    # Collect the required imports based on fields
    imports = set()
    for field in fields:
        data_type = field['dataType'].lower() if field['dataType'] else ''
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
    content = f"{import_statement}{base_import}\n\nclass {model_name_pascal}(Base):\n    __tablename__ = '{model_name_plural.lower()}'\n"

    for field in fields:
        data_type = field['dataType'].lower() if field['dataType'] else ''
        sqlalchemy_type = type_mapping.get(
            data_type, {'name': 'String'})  # Default to 'String'
        column_type_name = sqlalchemy_type['name']
        column_args = f"({sqlalchemy_type['length']})" if 'length' in sqlalchemy_type is not None else '(255)' if column_type_name == 'String' else ''

        if column_type_name == 'Integer':
            column_args = ''
            # check primary and autoIncrements here
            if field.get('isPrimaryKey', False):
                column_args += ", primary_key=True"
                if field.get('autoIncrements', False):
                    column_args += ", autoincrement=True"
            content += f"    {field['name']} = Column({column_type_name}{column_args})\n"

        else:
            if field.get('isPrimaryKey', False):
                column_args += ", primary_key=True"
            content += f"    {field['name']} = Column({column_type_name}{column_args})\n"

    # Add timestamp fields if specified in options
    if options and options.get('timestamps'):
        content += "    created_at = Column(DateTime, default=datetime.utcnow)\n"
        content += "    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)\n"
        # Add import for DateTime and datetime
        content = f"from datetime import datetime\n{import_statement}from sqlalchemy import DateTime\n" + \
            base_import + "\n" + content

    # Ensure the models directory exists
    directory_path = os.path.join(os.getcwd(), 'app', 'models')
    create_directory_if_not_exists(directory_path)

    # Write the generated model content to a Python file
    model_filename = f'{model_name_singular.lower()}.py'
    model_filepath = os.path.join(directory_path, model_filename)
    with open(model_filepath, 'w') as f:
        f.write(content)

 # Update __init__.py to include import statement for the new model
    init_py_path = os.path.join(directory_path, '__init__.py')
    with open(init_py_path, 'a') as init_py:
        if not content.endswith('\n'):
            init_py.write('\n')
        init_py.write(f"from .{model_filename[:-3]} import {model_name_pascal}\n")

    # Finally, run Alembic commands to manage database migrations
    try:
        subprocess.run(['alembic', 'revision', '--autogenerate', '-m', f"added {model_name_singular.lower()} table"], check=True)
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Alembic commands: {e}")
        return False