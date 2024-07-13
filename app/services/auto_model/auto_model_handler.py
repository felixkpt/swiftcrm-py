# auto_page_handler.py

from .model_generator import ModelGenerator
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db

def auto_model_handler(data: AutoPageBuilderRequest, db: Session = Depends(get_db)):
    try:
        print("STEP 1: Starting model generation\n")
        res = ModelGenerator(data, db).generate_model()
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
        else:
            print("Model generation failed, stopping process.\n")
    except Exception as e:
        print(f"Error in auto_model_handler: {e}\n")
        raise e
