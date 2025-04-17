import os
import sys
import importlib

# Ensure project root is in the PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)

# Point to modules directory instead of models
modules_directory = os.path.join(project_root, 'app', 'modules')

def recursive_import(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_model.py'):
                module_path = os.path.relpath(os.path.join(root, file), project_root).replace(os.sep, '.')
                module_name = module_path[:-3]  # Remove '.py'
                importlib.import_module(module_name)

recursive_import(modules_directory)
