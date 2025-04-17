from app.modules.auto_builders.model_builder.services.saves_file import handler
from app.modules.auto_builders.model_builder.services.repo_gen.content_templates.default_template import get_default_content
from app.modules.auto_builders.model_builder.services.repo_gen.content_templates import get_custom_content

def generate_repo(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_dotnotation = data['api_endpoint_dotnotation']
    fields = data['fields']
    nameSingular = data['nameSingular'].replace('-', '_')
    model_name_pascal = data['model_name_pascal']
    className = data['className']

    inserts_args1 = ""
    for field in fields:
        if field['name'] == 'user_id':
            inserts_args1 += f"            {field['name']} = current_user_id,\n"
        elif field['name'] == 'created_at' or field['name'] == 'updated_at':
            inserts_args1 += f"            {field['name']} = current_time,\n"
        elif field['name'] != 'id':
            if field['dataType'] in ['string', 'textarea']:
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
            if field['dataType'] in ['string', 'textarea']:
                inserts_args2 += f"            db_query.{field['name']} = str(model_request.{field['name']}).strip()\n"
            else:
                inserts_args2 += f"            db_query.{field['name']} = model_request.{field['name']}\n"

    repo_specific_filters = ""
    for field in fields:
        if field['type'] == 'input' or field['name'].endswith('_id'):
            if field['name'].endswith('_id'):
                repo_specific_filters += f"        value = query_params.get('{field['name']}', None)\n"
                repo_specific_filters += f"        if value is not None and value.isdigit():\n"
                repo_specific_filters += f"            query = query.filter(Model.{field['name']} == int(value))\n"
                # repo_specific_filters += f"            search_fields.remove('{field['name']}')\n"

            else:
                repo_specific_filters += f"        value = query_params.get('{field['name']}', '').strip()\n"
                repo_specific_filters += f"        if isinstance(value, str) and len(value) > 0:\n"
                repo_specific_filters += f"            query = query.filter(Model.{field['name']}.ilike(f'%{{value}}%'))\n"
                # repo_specific_filters += f"            search_fields.remove('{field['name']}')\n"

    model_path_name = nameSingular.lower() + '_model'

    customs = ['model_builder']

    if nameSingular.replace('-', '_').lower() in customs:
        print(f"{nameSingular} is a custom content type.")
        content = get_custom_content(api_endpoint_dotnotation, model_path_name, className, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2, nameSingular)
    else:
        print(f"{nameSingular} is using default content type.")
        content = get_default_content(api_endpoint_dotnotation, model_path_name, className, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2)

    # Check if content is None or empty, and raise an error if so
    if not content:
        raise ValueError(f"No content generated for {nameSingular}. Aborting the process.")

    # Write the generated repo content to a Python file
    path = api_endpoint.replace('-', '_')
    filename = f'{nameSingular.lower()}_repo.py'
    handler(path, 'modules', filename, content)

    return True
