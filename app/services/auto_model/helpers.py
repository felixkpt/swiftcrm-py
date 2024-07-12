import inflect
from app.services.str import STR

def get_model_names(model_name):
    # Convert modelName to slug with underscore and capitalize
    model_name_slug = STR.slug(model_name).capitalize()

    # Singularize the model_name if possible, otherwise use as is
    singularized = inflect.engine().singular_noun(model_name_slug)
    model_name_singular = singularized or model_name_slug

    # PascalCase conversion for singular model name
    model_name_pascal = STR.pascal(model_name_singular)

    # Pluralize the singular model name to generate pluralized version
    model_name_plural = inflect.engine().plural(
        model_name_singular) if not singularized else model_name_slug

    print('model_name_slug::', model_name_singular,
          model_name_plural, model_name_pascal,)
    return model_name_singular, model_name_plural, model_name_pascal,

def generate_table_name(api_endpoint_slugged, model_name_plural):
    # Check if api_endpoint_slugged ends with model_name_plural
    if api_endpoint_slugged.endswith(model_name_plural):
        # Remove the trailing model_name_plural from api_endpoint_slugged
        api_endpoint_slugged = api_endpoint_slugged[:-
                                                    (len(model_name_plural)+1)]

    # Construct the table_name
    table_name = api_endpoint_slugged.replace(
        '.', '_') + '_' + model_name_plural

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

def generate_model_and_api_names(data):
    model_name = data.modelName
    api_endpoint = data.apiEndpoint
    model_name_singular, model_name_plural, model_name_pascal = get_model_names(model_name)

    api_endpoint_slugged = api_endpoint.replace('/', '.').replace('-', '_')
    
    table_name = generate_table_name(api_endpoint_slugged.replace('.', '_'), model_name_plural.lower())
    class_name = generate_class_name(api_endpoint_slugged.replace('.', '-'), model_name_singular.lower())

    fields = data.fields or None

    return {
        'model_name': model_name,
        'api_endpoint': api_endpoint,
        'model_name_singular': model_name_singular,
        'model_name_plural': model_name_plural,
        'model_name_pascal': model_name_pascal,
        'api_endpoint_slugged': api_endpoint_slugged,
        'table_name': table_name,
        'class_name': class_name,
        'fields': fields,
    }

    