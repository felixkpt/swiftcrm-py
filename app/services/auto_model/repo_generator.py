from app.services.auto_model.saves_file import handler
from app.services.str import STR


def generate_repo(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_slugged = data['api_endpoint_slugged']
    fields = data['fields']
    model_name_singular = data['model_name_singular']
    model_name_pascal = data['model_name_pascal']
    class_name = data['class_name']

    inserts_args1 = ""
    for field in fields:
        if field.name == 'created_at' or field.name == 'updated_at':
            inserts_args1 += f"            {field.name}=current_time,\n"
        elif field.name != 'id':
            inserts_args1 += f"            {field.name}=model_request.{field.name},\n"

    inserts_args2 = ""
    for field in fields:
        if field.name == 'updated_at':
            inserts_args2 += f"            db_query.{field.name} = current_time\n"
        elif field.name != 'id' and field.name != 'created_at':
            inserts_args2 += f"            db_query.{field.name} = model_request.{field.name}\n"

    model_path_name = model_name_singular.lower()
    content = f"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.{api_endpoint_slugged+'.'+model_path_name} import {class_name} as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.requests.schemas.query_params import QueryParams  # Importing QueryParams for pagination and search
from app.services.search_repo import search_and_sort  # Importing function for searching and sorting

class {model_name_pascal}Repo:

    @staticmethod
    def list(db: Session, query_params: QueryParams):   
        search_fields = {[field.name for field in fields if field.isRequired]}
        query = db.query(Model)
        query = search_and_sort(query, Model, search_fields, query_params)

        skip = (query_params.page - 1) * query_params.limit
        query = query.offset(skip).limit(query_params.limit)

        return query.all()

    @staticmethod
    def get(db: Session, model_id: int):
        return db.query(Model).filter(Model.id == model_id).first()

    @staticmethod
    def create(db: Session, model_request):
        required_fields = {[field.name for field in fields if field.isRequired]}
        unique_fields = {[field.name for field in fields if field.isUnique]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
{inserts_args1}        )
        db.add(db_query)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create record. Possibly due to unique constraint."
            )
        db.refresh(db_query)
        return db_query

    @staticmethod
    def update(db: Session, model_id: int, model_request):
        required_fields = {[field.name for field in fields if field.isRequired]}
        unique_fields = {[field.name for field in fields if field.isUnique]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
{inserts_args2}            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found."
            )

    @staticmethod
    def delete(db: Session, model_id: int):
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            return True
        return False
"""

    # Write the generated repo content to a Python file
    path = api_endpoint.replace('-', '_')
    filename = f'{model_name_singular.lower()}_repo.py'
    handler(path, 'repositories', filename, content)

    return True
