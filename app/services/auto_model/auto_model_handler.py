from .model_generator import generate_model
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest


def prepare_generate_model(api_endpoint, model_name, fields):
    options = {'timestamps': True}
    # Assuming fields is a list of FieldSchema objects
    fields_dict_list = [
        {
            "name": field.name,
            "type": field.type,
            "label": field.label,
            "isRequired": field.isRequired,
            "dataType": field.dataType,
            "defaultValue": field.defaultValue,
            # Default to False if attribute is not present
            "isPrimaryKey": getattr(field, 'isPrimaryKey', False),
            "isUnique": getattr(field, 'isUnique', False),
            # Default to False if attribute is not present
            "autoIncrements": getattr(field, 'autoIncrements', False),
        }
        for field in fields
    ]

    return generate_model(api_endpoint, model_name, fields_dict_list, options)


def auto_model_handler(data: AutoPageBuilderRequest):
    model_name = data.modelName

    api_endpoint = data.apiEndpoint
    fields = data.fields

    res = prepare_generate_model(api_endpoint, model_name, fields)

    if res:
        generate_repo(api_endpoint, model_name, fields)
        generate_schema(api_endpoint, model_name, fields)
        generate_routes(api_endpoint, model_name)
