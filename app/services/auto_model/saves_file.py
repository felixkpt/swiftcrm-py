import os


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def handler(api_endpoint, relative_folder, filename, content):
    # Determine the directory path based on api_endpoint
    directory_path = os.path.join(
        os.getcwd(), 'app', relative_folder, *api_endpoint.split('/'))
    create_directory_if_not_exists(directory_path)

    # Create the route file
    file_path = os.path.join(directory_path, filename)

    with open(file_path, 'w') as f:
        f.write(content)
    return directory_path
