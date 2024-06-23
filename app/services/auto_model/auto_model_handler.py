from .model_generator import generate_model
from .routes_generator import generate_routes
from .schema_generator import generate_schema
import inflect


def prepare_generate_model(model_name, model_name_pluralized, fields):
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
            # Default to False if attribute is not present
            "autoIncrements": getattr(field, 'autoIncrements', False),
        }
        for field in fields
    ]

    return generate_model(model_name, model_name_pluralized, fields_dict_list, options)


def auto_model_handler(data):
    model_name = data.modelName
    model_name = model_name.capitalize()

    # Initialize inflect engine
    p = inflect.engine()
    # Check if model_name is already plural
    if not p.singular_noun(model_name):
        model_name_pluralized = p.plural(model_name)
    else:
        model_name_pluralized = model_name

    api_endpoint = data.apiEndpoint
    fields = data.fields

    res = prepare_generate_model(
        model_name, model_name_pluralized, fields)

    if res == True:
        # generate_crud(model_name, model_name_pluralized, fields)
        generate_schema(model_name, fields)
        generate_routes(model_name, model_name_pluralized, api_endpoint)
