import inflect
from app.services.str import STR
import hashlib


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
	nameSingular = singularized or cleaned_name

	# Convert singular model name to PascalCase
	model_name_pascal = STR.pascal(nameSingular)

	# Pluralize the singular model name to generate pluralized version
	namePlural = inflect.engine().plural(
		nameSingular) if not singularized else cleaned_name

	return nameSingular, namePlural, model_name_pascal


def generate_deterministic_random_string(input_string, length=5):
	"""
	Generate a deterministic random string based on the input string.
	
	Args:
	    input_string (str): The input string to seed the random generation.
	    length (int, optional): Length of the random string. Defaults to 4.
	
	Returns:
	    str: A deterministic random string of specified length.
	"""
	# Create a hash of the input string
	hash_object = hashlib.md5(input_string.encode())
	hash_hex = hash_object.hexdigest()

	# Use a slice of the hash to generate the random string
	random_string = hash_hex[:length - 3] # Leave space for the 3 letters

	# Prepend the 3 characters of the input_string
	first_char = input_string[:3]
	deterministic_string = first_char + random_string[:length - 3]

	# Ensure the string is the correct length
	return deterministic_string[:length].capitalize()


def trim_name(name, seed_name=None, max_length=55):
	"""
	Trim a name to a specified maximum length, prepending a deterministic random string if trimmed.
	
	Args:
	    name (str): The original name.
	    max_length (int, optional): Maximum length of the trimmed name. Defaults to 56.
	
	Returns:
	    str: The trimmed name.
	"""
	if len(name) > max_length:
		random_string = generate_deterministic_random_string(seed_name or name)
		trimmed_name = random_string + \
			name[-(max_length - len(random_string)):]
		return trimmed_name
	return name


def generate_class_and_tbl_names(api_endpoint, nameSingular, namePlural):
	"""
	Generate class and table names based on API endpoint and model names.
	
	Args:
	    api_endpoint (str): The API endpoint.
	    nameSingular (str): Singular form of the model name.
	    namePlural (str): Plural form of the model name.
	
	Returns:
	    dict: A dictionary containing class name, singular table name, and plural table name.
	"""
	api_endpoint = api_endpoint.lower()
	nameSingular = nameSingular.lower()
	namePlural = namePlural.lower()

	# Remove trailing namePlural from api_endpoint if present
	if api_endpoint.endswith(namePlural):
		res = api_endpoint[:-(len(namePlural) + 1)]
		if len(res) > 0:
			api_endpoint = res

	parts = api_endpoint.split('/')
	other_segments = '/'.join(parts[:-1]) # Join all parts except the last one
	last_segment = parts[-1].lower().replace('-', '_')

	nameSingular = nameSingular.replace('-', '_')
	namePlural = namePlural.replace('-', '_')

	are_similar = last_segment == nameSingular or last_segment == namePlural

	if are_similar:
		other = other_segments.replace('/', '_').replace('.', '_')
		className = other + ' ' + nameSingular

		if other:
			tableNameSingular = STR.slug(f"{other}_{nameSingular}")
			tableNamePlural = STR.slug(f"{other}_{namePlural}")
		else:
			tableNameSingular = nameSingular
			tableNamePlural = namePlural
	else:
		api_cleaned = STR.slug(api_endpoint)
		className = api_cleaned + '_' + nameSingular
		tableNameSingular = api_cleaned + '_' + nameSingular
		tableNamePlural = api_cleaned + '_' + namePlural

	print("api_endpoint", api_endpoint)
	print("tableNamePlural", tableNamePlural)

	# Convert the className to PascalCase
	limit = 50
	className = trim_name(STR.pascal(className), tableNameSingular, limit)
	tableNameSingular = trim_name(tableNameSingular, None, limit).lower()
	tableNamePlural = trim_name(tableNamePlural, None, limit).lower()

	return {
		'className': className,
		'tableNameSingular': tableNameSingular,
		'tableNamePlural': tableNamePlural
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
	api_endpoint_dotnotation = api_endpoint.strip('/').replace('/', '.').replace('-', '_')

	nameSingular, namePlural, model_name_pascal = get_model_names(model_name)

	res = generate_class_and_tbl_names(
		api_endpoint, nameSingular, namePlural)

	className = res['className']
	tableNameSingular = res['tableNameSingular']
	tableNamePlural = res['tableNamePlural']

	fields = data.fields or None

	return {
		'api_endpoint': api_endpoint,
		'api_endpoint_dotnotation': api_endpoint_dotnotation,
		'model_name': model_name,
		'nameSingular': nameSingular,
		'namePlural': namePlural,
		'model_name_pascal': model_name_pascal,
		'tableNameSingular': tableNameSingular,
		'tableNamePlural': tableNamePlural,
		'className': className,
		'fields': fields,
	}

def build_dot_namespace(api_endpoint_dotnotation, nameSingular):
	return api_endpoint_dotnotation + '.' + nameSingular.lower() if api_endpoint_dotnotation else nameSingular.lower()

