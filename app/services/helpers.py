import os
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from app.services.str import STR
import inflect
from langdetect import detect, LangDetectException


def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException as e:
        print(f"Error detecting language: {e}")
        return False


def filter_english_messages(messages, limit=5):
    english_messages = []
    english_count = 0

    index = 0
    while english_count < limit and index < len(messages):
        message = messages[index]
        if is_english(message['content']):
            english_messages.append(message)
            english_count += 1
        index += 1

    return english_messages


def format_error(key, detail):
    return [{"loc": ["body", key], "msg": detail}]


def generate_model_files(data: AutoPageBuilderRequest):
    modelName = data.modelName
    modelURI = data.modelURI
    fieldsRaw = data.fields

    print('AutoPageBuilderRequest::', modelName, modelURI, fieldsRaw)

    singularModelName = modelName.capitalize()
    listDirPath = os.path.join(
        os.getcwd(), 'app', 'pages', 'dashboard', modelURI)

    os.makedirs(listDirPath, exist_ok=True)

    # Generate Python model file
    generate_python_model(singularModelName, listDirPath, fieldsRaw)

    # Generate schema.sql file
    generate_schema_file(singularModelName, listDirPath, fieldsRaw)


def generate_python_model(singularModelName, listDirPath, fieldsRaw):
    filename = f"{singularModelName}.py"
    filepath = os.path.join(listDirPath, filename)

    with open(filepath, 'w') as f:
        f.write(f"class {singularModelName}:\n")
        for field in fieldsRaw:
            f.write(f"    {field.name} = '{field.defaultValue}'\n")


def generate_schema_file(singularModelName, listDirPath, fieldsRaw):
    filename = "schema.sql"
    filepath = os.path.join(listDirPath, filename)

    with open(filepath, 'w') as f:
        f.write(f"-- Schema for {singularModelName}\n")
        f.write(f"CREATE TABLE {singularModelName} (\n")
        for field in fieldsRaw:
            f.write(f"    {field.name} {map_data_type(field.dataType)},\n")
        f.write(f");\n")


def map_data_type(data_type):
    if data_type == 'integer':
        return 'INT'
    elif data_type == 'string':
        return 'VARCHAR(255)'
    elif data_type == 'longtext':
        return 'TEXT'
    else:
        # Default to VARCHAR(255) if data type is unknown
        return 'VARCHAR(255)'


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
