from app.services.auto_model.saves_file import handler
from app.services.auto_model.repo_gen.content_templates.default_template import get_default_content
from app.services.auto_model.repo_gen.content_templates import get_custom_content

def generate_repo(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_slugged = data['api_endpoint_slugged']
    fields = data['fields']
    name_singular = data['name_singular'].replace('-', '_')
    model_name_pascal = data['model_name_pascal']
    class_name = data['class_name']

    inserts_args1 = ""
    for field in fields:
        if field['name'] == 'user_id':
            inserts_args1 += f"            {field['name']} = current_user_id,\n"
        elif field['name'] == 'created_at' or field['name'] == 'updated_at':
            inserts_args1 += f"            {field['name']} = current_time,\n"
        elif field['name'] != 'id':
            if field['dataType'] == 'string' or field['dataType'] == 'textarea':
                inserts_args1 += f"            {field['name']} = str(model_request.{field['name']}).strip(),\n"
            else:
                inserts_args1 += f"            {field['name']} = model_request.{field['name']},\n"

    inserts_args2 = ""
    for field in fields:
        if field['name'] == 'updated_at':
            inserts_args2 += f"            db_query.{field['name']} = current_time\n"
        elif field['name'] == 'user_id':
            inserts_args2 += f"            db_query.{field['name']} = current_user_id\n"
        elif field['name'] != 'id' and field['name'] != 'created_at':
            if field['dataType'] == 'string' or field['dataType'] == 'textarea':
                inserts_args2 += f"            db_query.{field['name']} = str(model_request.{field['name']}).strip()\n"
            else:
                inserts_args2 += f"            db_query.{field['name']} = model_request.{field['name']}\n"

    # Generate repo filter conditions
    added = False
    repo_specific_filters = ""
    for field in fields:
        if field['type'] == 'input' or (field['name'] != 'id' and field['name'].endswith('_id')):
            added = True
            if field['name'].endswith('_id'):
                repo_specific_filters += f"        value = query_params.get('{field['name']}', None)\n"
                repo_specific_filters += f"        if value is not None and value.isdigit():\n"
                repo_specific_filters += f"            query = query.filter(Model.{field['name']} == int(value))\n"
            else:
                repo_specific_filters += f"        value = query_params.get('{field['name']}', '').strip()\n"
                repo_specific_filters += f"        if isinstance(value, str) and len(value) > 0:\n"
                repo_specific_filters += f"            query = query.filter(Model.{field['name']}.ilike(f'%{{value}}%'))\n"

    if added:
        repo_specific_filters = '\n' + repo_specific_filters
    else:
        repo_specific_filters = ''

    model_path_name = name_singular.lower() + '_model'

    customs = ['model_builder']

    if name_singular.replace('-', '_') in customs:
        print(f"{name_singular} is a custom content type.")
        content = get_custom_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2, name_singular)
    else:
        content = get_default_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2)
    
    # Write the generated repo content to a Python file
    path = api_endpoint.replace('-', '_')
    filename = f'{name_singular.lower()}_repo.py'
    handler(path, 'repositories', filename, content)

    return True
