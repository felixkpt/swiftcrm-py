from .model_generator import generate_model
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
import inflect
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest


def prepare_generate_model(model_name, fields):
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

    return generate_model(model_name, fields_dict_list, options)


def auto_model_handler(data: AutoPageBuilderRequest):
    model_name = data.modelName.lower().capitalize()
    singularized = inflect.engine().singular_noun(model_name)
    model_name_singular = singularized or model_name

    # Capitalize model_name_singular to match class naming convention
    model_name_singular = model_name_singular

    # Pluralize the model_name_singular to generate model_name_pluralized
    model_name_pluralized = inflect.engine().plural(
        model_name_singular) if not singularized else model_name

    api_endpoint = data.apiEndpoint
    fields = data.fields

    res = prepare_generate_model(model_name_singular, fields)

    if res:
        generate_repo(model_name_singular, model_name_pluralized, fields)
        generate_schema(model_name_singular, fields)
        generate_routes(model_name_singular,
                        model_name_pluralized, api_endpoint)
