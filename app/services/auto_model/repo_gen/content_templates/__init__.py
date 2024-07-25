import os

def get_custom_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2, name_singular):
    # Assuming `name_singular` represents a filename or resource identifier

    # Step 1: Construct the file path using `name_singular`
    file_path = f"{name_singular.replace('-', '_')}_template.py"

    # Step 2: Check if the file exists
    if os.path.exists(file_path):
        # Step 3: If the file exists, attempt to call `get_content` function
        try:
            module = __import__(file_path)
            if callable(getattr(module, 'get_content', None)):
                return module.get_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2)
        except ImportError as e:
            # Handle import errors if necessary
            print(f"Error importing {file_path}: {e}")
        except AttributeError:
            # `get_content` function not found in module
            pass
    else:
        print(f"File {file_path} not found.")

    # Step 4: Return None or handle when `get_content` function is not found or file doesn't exist
    return None
