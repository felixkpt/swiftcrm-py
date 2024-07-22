import inflect
from app.services.str import STR
import random
import string

def get_model_names(model_name):
    """
    Generate different name formats for a given model name.
    
    Args:
        model_name (str): The original model name.
    
    Returns:
        tuple: A tuple containing the singular model name, plural model name, and PascalCase model name.
    """
    # Convert modelName to slug with hyphens and capitalize
    cleaned_name = STR.slug(model_name, '-').capitalize()

    # Singularize the model_name if possible, otherwise use as is
    singularized = inflect.engine().singular_noun(cleaned_name)
    name_singular = singularized or cleaned_name

    # Convert singular model name to PascalCase
    model_name_pascal = STR.pascal(name_singular)

    # Pluralize the singular model name to generate pluralized version
    name_plural = inflect.engine().plural(name_singular) if not singularized else cleaned_name

    return name_singular, name_plural, model_name_pascal

def generate_random_string(length=4):
    """
    Generate a random string of lowercase letters.
    
    Args:
        length (int, optional): Length of the random string. Defaults to 4.
    
    Returns:
        str: A random string of specified length.
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def trim_name(name, max_length=56):
    """
    Trim a name to a specified maximum length, prepending a random string if trimmed.
    
    Args:
        name (str): The original name.
        max_length (int, optional): Maximum length of the trimmed name. Defaults to 56.
    
    Returns:
        str: The trimmed name.
    """
    if len(name) > max_length:
        random_string = generate_random_string()
        trimmed_name = random_string + name[-(max_length - 4):]
        return trimmed_name
    return name

def generate_class_and_tbl_names(api_endpoint, name_singular, name_plural):
    """
    Generate class and table names based on API endpoint and model names.
    
    Args:
        api_endpoint (str): The API endpoint.
        name_singular (str): Singular form of the model name.
        name_plural (str): Plural form of the model name.
    
    Returns:
        dict: A dictionary containing class name, singular table name, and plural table name.
    """
    api_endpoint = api_endpoint.lower()
    name_singular = name_singular.lower()
    name_plural = name_plural.lower()

    # Remove trailing name_plural from api_endpoint if present
    if api_endpoint.endswith(name_plural):
        res = api_endpoint[:-(len(name_plural) + 1)]
        if len(res) > 0:
            api_endpoint = res

    parts = api_endpoint.split('/')
    other_segments = '/'.join(parts[:-1])  # Join all parts except the last one
    last_segment = parts[-1].lower().replace('-', '_')

    are_similar = last_segment == name_plural

    name_singular = name_singular.replace('-', '_')
    name_plural = name_plural.replace('-', '_')

    if are_similar:
        class_name = other_segments.replace('/', ' ').replace('.', ' ') + ' ' + name_singular
        table_name_singular = name_singular
        table_name_plural = name_plural
    else:
        api_cleaned = STR.slug(api_endpoint)
        class_name = api_cleaned + '_' + name_singular
        table_name_singular = api_cleaned + '_' + name_singular
        table_name_plural = api_cleaned + '_' + name_plural

    # Convert the class_name to PascalCase
    class_name = trim_name(STR.pascal(class_name))
    table_name_singular = trim_name(table_name_singular)
    table_name_plural = trim_name(table_name_plural)

    return {
        'class_name': class_name,
        'table_name_singular': table_name_singular,
        'table_name_plural': table_name_plural
    }

def generate_model_and_api_names(data):
    """
    Generate model and API names based on input data.
    
    Args:
        data (object): Data containing model display name and API endpoint.
    
    Returns:
        dict: A dictionary containing various name formats and fields.
    """
    model_name = data.modelDisplayName
    api_endpoint = data.apiEndpoint
    api_endpoint_slugged = api_endpoint.replace('/', '.').replace('-', '_')

    name_singular, name_plural, model_name_pascal = get_model_names(model_name)

    res = generate_class_and_tbl_names(api_endpoint, name_singular, name_plural)

    class_name = res['class_name']
    table_name_singular = res['table_name_singular']
    table_name_plural = res['table_name_plural']

    fields = data.fields or None

    return {
        'api_endpoint': api_endpoint,
        'api_endpoint_slugged': api_endpoint_slugged,
        'model_name': model_name,
        'name_singular': name_singular,
        'name_plural': name_plural,
        'model_name_pascal': model_name_pascal,
        'table_name_singular': table_name_singular,
        'table_name_plural': table_name_plural,
        'class_name': class_name,
        'fields': fields,
    }
