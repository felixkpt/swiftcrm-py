from app.services.auto_model.saves_file import handler


def generate_repo(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_slugged = data['api_endpoint_slugged']
    fields = data['fields']
    name_singular = data['name_singular']
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

    # Generate filter conditions
    added = False
    filter_conditions = ""
    for field in fields:
        if field.name != 'id' and field.name.endswith('_id'):
            added = True
            filter_conditions += f"        value = query_params.get('{field.name}', None)\n"
            filter_conditions += f"        if value is not None:\n"
            filter_conditions += f"            query = query.filter(Model.{field.name} == value)\n"
    if added:
        filter_conditions = '\n' + filter_conditions
    else:
        filter_conditions = ''

    model_path_name = name_singular.lower()
        
    content = f"""
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.{api_endpoint_slugged+'.'+model_path_name} import {class_name} as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_filters, add_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo

class {model_name_pascal}Repo(BaseRepo):
    
    model = Model

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = {[field.name for field in fields if field.isRequired]}

        query = db.query(Model)
        query = apply_filters(query, Model, search_fields, query_params)
{filter_conditions}
        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        metadata = add_metadata(query, query_params)
        
        results = {{
            "data": query.all(),
            "metadata": metadata
        }}

        return results

    def create(self, db: Session, model_request):
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
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    def update(self, db: Session, model_id: int, model_request):
        required_fields = {[field.name for field in fields if field.isRequired]}
        unique fields = {[field.name for field in fields if field.isUnique]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
{inserts_args2}            db.commit()
            db.refresh(db_query)
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
"""

    # Write the generated repo content to a Python file
    path = api_endpoint.replace('-', '_')
    filename = f'{name_singular.lower()}_repo.py'
    handler(path, 'repositories', filename, content)

    return True
