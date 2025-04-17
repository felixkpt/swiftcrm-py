# app/services/auto_model/repo_gen/content_templates/__init__.py
import importlib

def get_custom_content(api_endpoint_dotnotation, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2, name_singular):
    # Convert name_singular to a module-friendly filename
    module_name = f"{name_singular.replace('-', '_').lower()}_template"

    # Define the module path
    module_path = f"app.modules.auto_builders.auto_model.repo_gen.content_templates.{module_name}"
    
    # Attempt to import and use the specified template module
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, 'get_content') and callable(module.get_content):
            return module.get_content(api_endpoint_dotnotation, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2)
        else:
            print(f"'get_content' function not found in module '{module_path}'.")
    except ModuleNotFoundError:
        print(f"Module '{module_path}' not found.")
    except Exception as e:
        print(f"An error occurred while trying to import '{module_path}': {e}")

    return None
