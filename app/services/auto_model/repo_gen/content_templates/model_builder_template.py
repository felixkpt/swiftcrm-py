def get_content(api_endpoint_slugged, model_path_name, class_name, model_name_pascal, fields, repo_specific_filters, inserts_args1, inserts_args2):
    content = f"""
from datetime import datetime
from sqlalchemy.orm import joinedload
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.auto_builders.model_builder.model_builder_model import AdminAutoBuildersModelBuilder as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.repositories.admin.auto_builders.model_builder.model_fields.model_field_repo import ModelFieldRepo
from app.repositories.admin.auto_builders.model_builder.model_headers.model_header_repo import ModelHeaderRepo
from app.repositories.admin.auto_builders.model_builder.action_labels.action_label_repo import ActionLabelRepo


class {model_name_pascal}Repo(BaseRepo):

    model = Model
    notification = NotificationService()

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}

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
        required_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}
        unique_fields = {[field['name'] for field in fields if field.get('isUnique', False)]}
        
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = Model(
{inserts_args1}        )
        db.add(db_query)
        try:
            db.commit()
            {inserts_related()}
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
        except IntegrityError as e:
            db.rollback()
            return ResponseHelper.handle_integrity_error(e)
        db.refresh(db_query)
        return db_query


    async def update(self, db: Session, model_id: int, model_request):
        required_fields = {[field['name'] for field in fields if field.get('isRequired', False)]}
        unique_fields = {[field['name'] for field in fields if field.get('isUnique', False)]}
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        current_user_id = user().id
        db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
        if db_query:
{inserts_args2}            db.commit()
            db.refresh(db_query)

            {updates_related()}

            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')

            # Convert the model to a dictionary
            model_data = {{column.name: getattr(
                db_model, column.name) for column in db_model.__table__.columns}}

            # Combine and return the updated model with its related objects
            combined_result = {{
                **model_data,
                "fields": created_fields,
                "headers": created_headers,
                "action_labels": created_action_labels
            }}
            return combined_result

        return ResponseHelper.handle_not_found_error(model_id)

    @staticmethod
    def get(db: Session, model_id: int):
        print('model_id, mod', model_id)
        return db.query(Model). \
            options(
                joinedload(Model.fields),
                joinedload(Model.action_labels),
                joinedload(Model.headers)
        ). \
            filter(Model.id == model_id). \
            first()

    def get_page_by_name(db: Session, name_singular: str):
        return db.query(Model).filter(Model.name_singular == name_singular).first()

    def get_page_by_table_name(db: Session, table_name_singular: str):
        return db.query(Model).filter(Model.table_name_singular == table_name_singular).first()

    def get_page_by_table_name_plural(db: Session, table_name_plural: str):
        return db.query(Model).filter(Model.table_name_plural == table_name_plural).first()

    def get_page_by_apiEndpoint(db: Session, apiEndpoint: str):
        return db.query(Model).filter(Model.apiEndpoint == apiEndpoint).first()
"""

    return content


def inserts_related():
    return """
            db.refresh(new_model)
            # Store fields, headers, and action labels using their respective repositories
            created_fields = []
            for field in model_request.fields:
                field.model_builder_id = new_model.id
                created_field = await ModelFieldRepo().create(db, field)
                created_fields.append(created_field)

            created_headers = []
            for header in model_request.headers:
                header.model_builder_id = new_model.id
                created_header = await ModelHeaderRepo().create(db, header)
                created_headers.append(created_header)

            created_action_labels = []
            for action_label in model_request.actionLabels:
                action_label.model_builder_id = new_model.id
                created_action_label = await ActionLabelRepo().create(db, action_label)
                created_action_labels.append(created_action_label)
            """


def updates_related():
    return """
            # Clear existing fields, headers, and action labels
            db.query(ModelFieldRepo.model).filter(
                ModelFieldRepo.model.model_builder_id == model_id).delete()
            db.query(ModelHeaderRepo.model).filter(
                ModelHeaderRepo.model.model_builder_id == model_id).delete()
            db.query(ActionLabelRepo.model).filter(
                ActionLabelRepo.model.model_builder_id == model_id).delete()
            db.commit()

            # Store updated fields, headers, and action labels
            created_fields = []
            for field in model_request.fields:
                field.model_builder_id = model_id
                created_field = await ModelFieldRepo().create(db, field)
                created_fields.append(created_field)

            created_headers = []
            for header in model_request.headers:
                header.model_builder_id = model_id
                created_header = await ModelHeaderRepo().create(db, header)
                created_headers.append(created_header)

            created_action_labels = []
            for action_label in model_request.actionLabels:
                action_label.model_builder_id = model_id
                created_action_label = await ActionLabelRepo().create(db, action_label)
                created_action_labels.append(created_action_label)
                """
