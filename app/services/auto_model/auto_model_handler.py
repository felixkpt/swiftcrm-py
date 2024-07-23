import subprocess
from .model_generator import ModelGenerator
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.admin.auto_builders.model_builder.model_builder_request import ModelBuilderRequest
from app.requests.schemas.admin.auto_builders.model_builder.model_fields.model_field import ModelFieldSchema
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db


def convert_fields_to_dict(fields):
    """Convert each field in the list to a dictionary if it's not already."""
    return [field.dict() if isinstance(field, ModelFieldSchema) else field for field in fields]


def auto_model_handler(data: ModelBuilderRequest, db: Session = Depends(get_db), id: int = None):
    action_type = "create" if id is None else "edit"

    fields = convert_fields_to_dict(data.get('fields', []))

    if fields:
        if data['table_name_singular'] != 'users':
            fields.append({
                'name': 'user_id',
                'type': 'integer',
                'label': 'Creator',
                'isRequired': False,
                'dataType': 'integer'
            })

        fields.append({
            'name': 'created_at',
            'type': 'datetime',
            'label': 'Updated',
            'isRequired': False,
            'dataType': 'string'
        })

        fields.append({
            'name': 'updated_at',
            'type': 'datetime',
            'label': 'Updated',
            'isRequired': False,
            'dataType': 'string'
        })
        data['fields'] = fields

    print("STEP 1: Starting model generation\n")
    model_generator = ModelGenerator(data, db)
    res = model_generator.generate_model()
    print("STEP 1: Model generation completed\n")

    if res:
        print("STEP 2: Generating repository\n")
        generate_repo(data)
        print("STEP 2: Repository generation completed\n")

        print("STEP 3: Generating schema\n")
        generate_schema(data)
        print("STEP 3: Schema generation completed\n")

        print("STEP 4: Generating routes\n")
        generate_routes(data)
        print("STEP 4: Routes generation completed\n")

        # Run Git Add and Commit
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            commit_message = f"Autobuilder: {action_type.capitalize()} {data['name_singular'].lower()} model and related files"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("STEP 5: Git add and commit completed\n")
        except subprocess.CalledProcessError as e:
            print(f"Error running Git commands: {e}")
            raise e
    else:
        print("Model generation failed, stopping process.\n")
