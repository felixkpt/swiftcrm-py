import inflect
from app.services.str import STR


def get_model_names(model_name):
    # Convert modelName to slug with underscore and capitalize
    model_name_slug = STR.slug(model_name).capitalize()

    # Singularize the model_name if possible, otherwise use as is
    singularized = inflect.engine().singular_noun(model_name_slug)
    name_singular = singularized or model_name_slug

    # PascalCase conversion for singular model name
    model_name_pascal = STR.pascal(name_singular)

    # Pluralize the singular model name to generate pluralized version
    name_plural = inflect.engine().plural(
        name_singular) if not singularized else model_name_slug

    return name_singular, name_plural, model_name_pascal,


def generate_table_names(api_endpoint_slugged, name_singular, name_plural):
    # Check if api_endpoint_slugged ends with name_plural
    if api_endpoint_slugged.endswith(name_plural):
        # Remove the trailing name_plural from api_endpoint_slugged
        api_endpoint_slugged = api_endpoint_slugged[:-
                                                    (len(name_plural)+1)]

    # Construct the table_name
    table_name_singular = api_endpoint_slugged.replace(
        '.', '_') + '_' + name_singular
    table_name_plural = api_endpoint_slugged.replace(
        '.', '_') + '_' + name_plural

    return {'table_name_singular': table_name_singular, 'table_name_plural': table_name_plural}


def generate_class_name(api_endpoint, name_singular):
    # Remove trailing name_singular from api_endpoint if present
    if api_endpoint.endswith(name_singular):
        res = api_endpoint[:-(len(name_singular) + 1)]
        if len(res) > 0:
            api_endpoint = res

    parts = api_endpoint.split('/')
    other_segments = '/'.join(parts[:-1])  # Join all parts except the last one
    last_segment = parts[-1]
    last_segment_singular = (inflect.engine().singular_noun(
        last_segment) or last_segment).lower().replace('-', '_')

    # Singularize the last segment using inflect
    are_similar = last_segment_singular == name_singular.lower()

    # Construct the class_name by replacing '/' with '-' and appending name_singular
    if are_similar:
        class_name = other_segments.replace(
            '/', '-').replace('.', '-') + '_' + name_singular
    else:
        class_name = api_endpoint.replace(
            '/', '-').replace('.', '-') + name_singular

    # Convert the class_name to PascalCase
    class_name = STR.pascal(class_name)

    return class_name


def generate_model_and_api_names(data):
    model_name = data.name_singular or data.modelName
    api_endpoint = data.apiEndpoint
    name_singular, name_plural, model_name_pascal = get_model_names(
        model_name)

    api_endpoint_slugged = api_endpoint.replace('/', '.').replace('-', '_')
    tables = generate_table_names(
        api_endpoint_slugged.replace('.', '_'), name_singular.lower(), name_plural.lower(),)
    table_name_singular = tables['table_name_singular']
    table_name_plural = tables['table_name_plural']

    class_name = generate_class_name(api_endpoint, name_singular.lower())
   
    fields = data.fields or None

    return {
        'api_endpoint': api_endpoint,
        'model_name': model_name,
        'name_singular': name_singular,
        'name_plural': name_plural,
        'model_name_pascal': model_name_pascal,
        'api_endpoint_slugged': api_endpoint_slugged,
        'table_name_singular': table_name_singular,
        'table_name_plural': table_name_plural,
        'class_name': class_name,
        'fields': fields,
    }
