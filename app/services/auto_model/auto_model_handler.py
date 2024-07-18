import subprocess
from .model_generator import ModelGenerator
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

def auto_model_handler(data: AutoPageBuilderRequest, db: Session = Depends(get_db), id: int = None):
    action_type = "create" if id is None else "edit"
    model_generator = ModelGenerator(data, db)
    res = model_generator.generate_model()
    try:
        print("STEP 1: Starting model generation\n")
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

    except Exception as e:
        return
        # Stash changes if any step fails
        try:
            stash_message = f"Autobuilder: Stash changes due to {action_type.capitalize()} {data['name_singular'].lower()} failure - {str(e)}"
            subprocess.run(['git', 'stash', 'push', '-m', stash_message], check=True)
            print(f"Changes stashed: {stash_message}\n")
        except subprocess.CalledProcessError as stash_error:
            print(f"Error stashing changes: {stash_error}")

        print(f"Error in auto_model_handler: {e}\n")
        raise e
