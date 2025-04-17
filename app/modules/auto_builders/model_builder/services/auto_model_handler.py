import bcrypt
import subprocess
from .model_generator import ModelGenerator
from app.modules.auto_builders.model_builder.services.repo_gen.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.modules.users.user_model import User
from app.patterns.models.factory import ModelFactory
from app.modules.users.user_repo import UserRepo
import re

def convert_fields_to_dict(fields):
    """Convert each field in the list to a dictionary if it's not already."""
    return [field.dict() for field in fields]

def normalize_fields(fields: list[dict]) -> list[dict]:
    for field in fields:
        # Lowercase, replace spaces with underscores, remove non-alphanumeric (except _)
        name = field['name'].lower().replace(' ', '_')
        name = re.sub(r'[^a-z0-9_]', '', name)
        field['name'] = name
    return fields


async def auto_model_handler(data, db: Session = Depends(get_db), id: int = None):
    action_type = "create" if id is None else "edit"

    fields = convert_fields_to_dict(data.get('fields', []))

    if fields:
        fields = normalize_fields(fields)

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

    print(f"STEP 1: Starting model generation for: {data['table_name_plural']} \n")
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

        print('????',data['table_name_plural'] )
        if data['table_name_plural'] == 'users':
            print("SEEDING USER...")
            repo = UserRepo()
            try:
                factory = ModelFactory()
                # Insert an admin user
                user_data = {
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'email': 'adminuser@mail.com',
                    'phone_number': '+254712345678',
                    'password': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    'password_confirmation': bcrypt.hashpw('adminuser@mail.com'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                }
                user_instance = factory.create_instance(
                    User, **user_data)
                await repo.create(db, user_instance)
            except Exception as e:
                print("ERROR SEEDING USER:", e)

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
