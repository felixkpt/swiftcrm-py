import os
import importlib.util
from fastapi import FastAPI

# Import dynamically generated route modules
def auto_register_routes(app: FastAPI):
    routes_directory = os.path.join(os.getcwd(), 'app', 'routes')
    for root, _, files in os.walk(routes_directory):
        if "__init__.py" in files:
            files.remove("__init__.py")
        for filename in files:
            if filename.endswith('.py'):
                module_name = filename[:-3]  # Remove '.py' extension
                    # Calculate prefix based on the path relative to routes_directory
                prefix = os.path.relpath(
                    root, routes_directory).replace(os.sep, '/')
                if prefix.startswith('.'):
                    prefix = prefix[1:]
                if prefix.endswith('/'):
                    prefix = prefix[:-1]  # Remove trailing slash if present
                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(root, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if prefix:
                    prefix = prefix if not prefix.endswith(
                        '/') else prefix[:-1]
                    prefix = '/' + \
                        prefix if not prefix.startswith('/') else prefix
                else:
                    prefix = ''

                # Register the router with the calculated prefix and module name as tags
                app.include_router(
                    module.router, prefix=prefix, tags=[module_name])

