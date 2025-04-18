import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    # Create __init__.py files recursively starting from /app/
    app_directory = os.path.join(os.getcwd(), 'app')
    current_path = directory_path
    while current_path != app_directory and current_path.startswith(app_directory):
        init_file = os.path.join(current_path, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                pass
        current_path = os.path.dirname(current_path)

def generate_file_path(api_endpoint, relative_folder, filename):
    # Determine the directory path based on api_endpoint
    directory_path = os.path.join(
        os.getcwd(), 'app', relative_folder, *api_endpoint.split('/'))
    return {'directory_path': directory_path, 'file_path': os.path.join(directory_path, filename)}

def handler(api_endpoint, relative_folder, filename, content):
    res = generate_file_path(api_endpoint, relative_folder, filename)
    directory_path = res['directory_path']
    file_path = res['file_path']

    # Create the directory and file
    create_directory_if_not_exists(directory_path)
    with open(file_path, 'w') as f:
        f.write(content)
    return directory_path
