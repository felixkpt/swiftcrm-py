from .model_generator import ModelGenerator
from app.services.auto_model.repo_generator import generate_repo
from .schema_generator import generate_schema
from .routes_generator import generate_routes
from app.requests.schemas.auto_page_builder import AutoPageBuilderRequest
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db


def auto_model_handler(data: AutoPageBuilderRequest, db: Session = Depends(get_db)):

    res = ModelGenerator(data, db).generate_model()

    if res:
        generate_repo(data)
        generate_schema(data)
        generate_routes(data)
