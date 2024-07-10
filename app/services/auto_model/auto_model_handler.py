from .model_generator import generate_model
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from app.services.str import STR
from app.services.helpers import get_model_names


def generate_table_name(api_endpoint_slugged, model_name_plural):
    # Check if api_endpoint_slugged ends with model_name_plural
    if api_endpoint_slugged.endswith(model_name_plural):
        # Remove the trailing model_name_plural from api_endpoint_slugged
        api_endpoint_slugged = api_endpoint_slugged[:-
                                                    (len(model_name_plural)+1)]

    # Construct the table_name
    table_name = api_endpoint_slugged.replace(
        '.', '-') + '_' + model_name_plural

    return table_name

def generate_class_name(api_endpoint_slugged, model_name_singular):
    # Remove trailing model_name_singular from api_endpoint_slugged if present
    if api_endpoint_slugged.endswith(model_name_singular):
        api_endpoint_slugged = api_endpoint_slugged[:-(len(model_name_singular) + 1)]

    # Construct the class_name by replacing '.' with '-' and appending model_name_singular
    class_name = api_endpoint_slugged.replace('.', '-') + '_' + model_name_singular

    # Convert the class_name to PascalCase
    class_name = STR.pascal(class_name)
    return class_name

def auto_model_handler(data: AutoPageBuilderRequest):
    model_name = data.modelName

    api_endpoint = data.apiEndpoint
    fields = data.fields

    model_name_singular, model_name_plural, model_name_pascal = get_model_names(
        model_name)

    api_endpoint_slugged = api_endpoint.replace('/', '.').replace('-', '_')
    
    table_name = generate_table_name(
        api_endpoint_slugged.replace('.', '-'), model_name_plural.lower())
    class_name = generate_class_name(
        api_endpoint_slugged.replace('.', '-'), model_name_singular.lower())

    data = {
        'api_endpoint': api_endpoint,
        'api_endpoint_slugged': api_endpoint_slugged,
        'fields': fields,
        'model_name': model_name,
        'model_name_singular': model_name_singular,
        'model_name_plural': model_name_plural,
        'model_name_pascal': model_name_pascal,
        'table_name': table_name,
        'class_name': class_name,
    }

    res = generate_model(data)

    if res:
        generate_repo(data)
        generate_schema(data)
        generate_routes(data)
