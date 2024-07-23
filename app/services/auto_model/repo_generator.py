from app.services.auto_model.saves_file import handler

def generate_repo(data):
    api_endpoint = data['api_endpoint']
    api_endpoint_slugged = data['api_endpoint_slugged']
    fields = data['fields']
    name_singular = data['name_singular'].replace('-', '_')
    model_name_pascal = data['model_name_pascal']
    class_name = data['class_name']

    inserts_args1 = ""
    for field in fields:
        if field.name == 'created_at' or field.name == 'updated_at':
            inserts_args1 += f"            {field.name} = current_time,\n"
        elif field.name == 'user_id':
            inserts_args1 += f"            {field.name} = current_user_id,\n"
        elif field.name != 'id':
            if field.dataType == 'string' or field.dataType == 'textarea':
                inserts_args1 += f"            {field.name} = str(model_request.{field.name}).strip(),\n"
            else:
                inserts_args1 += f"            {field.name} = model_request.{field.name},\n"

    inserts_args2 = ""
    for field in fields:
        if field.name == 'updated_at':
            inserts_args2 += f"            db_query.{field.name} = current_time\n"
        elif field.name == 'user_id':
            inserts_args2 += f"            db_query.{field.name} = current_user_id\n"
        elif field.name != 'id' and field.name != 'created_at':
            if field.dataType == 'string' or field.dataType == 'textarea':
                inserts_args2 += f"            db_query.{field.name} = str(model_request.{field.name}).strip()\n"
            else:
                inserts_args2 += f"            db_query.{field.name} = model_request.{field.name}\n"

    # Generate repo filter conditions
    added = False
    repo_specific_filters = ""
    for field in fields:
        if field.type == 'input' or (field.name != 'id' and field.name.endswith('_id')):
            added = True
            if field.name.endswith('_id'):
                repo_specific_filters += f"        value = query_params.get('{field.name}', None)\n"
                repo_specific_filters += f"        if value is not None and value.isdigit():\n"
                repo_specific_filters += f"            query = query.filter(Model.{field.name} == int(value))\n"
            else:
                repo_specific_filters += f"        value = query_params.get('{field.name}', '').strip()\n"
                repo_specific_filters += f"        if isinstance(value, str) and len(value) > 0:\n"
                repo_specific_filters += f"            query = query.filter(Model.{field.name}.ilike(f'%{{value}}%'))\n"

    if added:
        repo_specific_filters = '\n' + repo_specific_filters
    else:
        repo_specific_filters = ''

    model_path_name = name_singular.lower()+'_model'

    content = f"""
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.{api_endpoint_slugged+'.'+model_path_name} import {class_name} as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.auth import user  # Import user function

class {model_name_pascal}Repo(BaseRepo):
    
    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = {[field.name for field in fields if field.isRequired]}

        query = db.query(Model)
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        # Get current user ID
        current_user_id = user(request).id
        query = query.filter(Model.user_id == current_user_id)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        results = {{
            "records": query.all(),
            "metadata": metadata
        }}

        return results

    def repo_specific_filters(self, query, Model, query_params):
{repo_specific_filters}
        return query

    async def create(self, db: Session, model_request):
        required_fields = {[field.name for field in fields if field.isRequired]}
        unique_fields = {[field.name for field in fields if field.isUnique]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
{inserts_args1}        )
        db.add(db_query)
        try:
            db.commit()
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query

    async def update(self, db: Session, model_id: int, model_request):
        required_fields = {[field.name for field in fields if field.isRequired]}
        unique_fields = {[field.name for field in fields if field.isUnique]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
{inserts_args2}            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
"""

    # Write the generated repo content to a Python file
    path = api_endpoint.replace('-', '_')
    filename = f'{name_singular.lower()}_repo.py'
    handler(path, 'repositories', filename, content)

    return True
