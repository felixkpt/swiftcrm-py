import os
import sys
import importlib

# Ensure the root of your project is in the PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

# Recursively import all models
models_directory = os.path.join(os.path.dirname(__file__))

def recursive_import(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                module_path = os.path.relpath(os.path.join(root, file), models_directory).replace(os.sep, '.')
                module_name = f'app.models.{module_path[:-3]}'  # Remove '.py' at the end
                importlib.import_module(module_name)

recursive_import(models_directory)
