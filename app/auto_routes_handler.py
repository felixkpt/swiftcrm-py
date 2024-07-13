import os
import importlib.util
from fastapi import FastAPI


def auto_register_routes(app: FastAPI):
    routes_directory = os.path.join(os.getcwd(), 'app', 'routes')
    register_files_in_directory(app, routes_directory)


def register_files_in_directory(app, directory_path):
    subdirectories = [d for d in os.listdir(
        directory_path) if os.path.isdir(os.path.join(directory_path, d))]

    # Process directories first
    for dir_name in subdirectories:
        subdirectory_path = os.path.join(directory_path, dir_name)
        register_files_in_directory(app, subdirectory_path)

    # Process files after directories
    files = [f for f in os.listdir(directory_path) if os.path.isfile(
        os.path.join(directory_path, f)) and f.endswith('.py') and f != '__init__.py']
    register_files(app, directory_path, files)


def register_files(app, root, files):
    for filename in files:
        # print('Registering...', root, filename)
        if filename.endswith('.py'):
            module_name = filename[:-3]  # Remove '.py' extension
            prefix = os.path.relpath(root, os.getcwd()).replace(os.sep, '/')
            if prefix.startswith('.'):
                prefix = prefix[1:]
            if prefix.endswith('/'):
                prefix = prefix[:-1]

            spec = importlib.util.spec_from_file_location(
                module_name, os.path.join(root, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'router'):
                if prefix:
                    prefix = '/' + \
                        prefix if not prefix.startswith('/') else prefix
                    prefix = str_after(prefix, 'app/routes')

                app.include_router(
                    module.router, prefix=prefix, tags=[module_name])
            else:
                print(
                    f"Module {module_name} does not define 'router' attribute. Skipping registration.")


def str_after(input_str, target):
    index = input_str.find(target)
    if index == -1:
        return input_str  # Target substring not found, return the whole string
    return input_str[index + len(target):]
