# app/services/auto_model/model_generator.py
import os
import subprocess
from app.services.auto_model.crud_generator import generate_crud
from app.services.auto_model.table_generator import generate_table


def generate_model(model_name, model_name_pluralized, fields, options=None):

    content, model_filepath, directory_path, model_filename = generate_table(
        model_name, fields, options)

    content += '\n'+generate_crud(model_name, model_name_pluralized, fields)

    with open(model_filepath, 'w') as f:
        f.write(content)

    # Update __init__.py to include import statement for the new model
    init_py_path = os.path.join(directory_path, '__init__.py')
    with open(init_py_path, 'r+') as init_py:
        # Read the content of __init__.py
        content = init_py.read()

        # Ensure there's a newline at the end of the file
        if content and content[-1] != '\n':
            init_py.write('\n')

        # Write the import statement
        init_py.write(f"from .{model_filename[:-3]} import {model_name}\n")

    # Finally, we need to run console commands for alembic
    try:
        subprocess.run(['alembic', 'revision', '--autogenerate',
                       '-m', f"added {model_name.lower()} table"], check=True)
        subprocess.run(['alembic', 'upgrade', 'head'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Alembic commands: {e}")
        return False
