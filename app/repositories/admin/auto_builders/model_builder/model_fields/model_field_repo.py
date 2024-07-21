
from datetime import datetime
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.admin.auto_builders.model_builder.model_fields.model_field import AdminAutoBuildersModelBuilderModelField as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.services.search_repo import get_query_params, apply_common_filters, set_metadata  # Importing functions for querying, searching and sorting
from app.requests.response.response_helper import ResponseHelper  # Importing ResponseHelper for consistent error handling
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService  # Import NotificationService


class ModelFieldRepo(BaseRepo):
    
    model = Model
    notification = NotificationService()  # Instantiate notification class

    async def list(self, db: Session, request: Request):
        query_params = get_query_params(request)
        search_fields = ['model_builder_id', 'name', 'type', 'label', 'dataType', 'defaultValue', 'isVisibleInList', 'isVisibleInSingleView', 'isRequired', 'isUnique', 'desktopWidth', 'mobileWidth']

        query = db.query(Model)
        
        query = apply_common_filters(query, Model, search_fields, query_params)
        query = self.repo_specific_filters(query, Model, query_params)
        metadata = set_metadata(query, query_params)

        skip = (query_params['page'] - 1) * query_params['per_page']
        query = query.offset(skip).limit(query_params['per_page'])

        
        results = {
            "records": query.all(),
            "metadata": metadata
        }

        return results

    def repo_specific_filters(self, query, Model, query_params):

        value = query_params.get('model_builder_id', None)
        if value is not None and value.isdigit():
            query = query.filter(Model.model_builder_id == int(value))
        value = query_params.get('name', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.name.ilike(f'%{value}%'))
        value = query_params.get('type', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.type.ilike(f'%{value}%'))
        value = query_params.get('label', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.label.ilike(f'%{value}%'))
        value = query_params.get('dataType', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.dataType.ilike(f'%{value}%'))
        value = query_params.get('defaultValue', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.defaultValue.ilike(f'%{value}%'))
        value = query_params.get('isVisibleInList', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.isVisibleInList.ilike(f'%{value}%'))
        value = query_params.get('isVisibleInSingleView', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.isVisibleInSingleView.ilike(f'%{value}%'))
        value = query_params.get('isRequired', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.isRequired.ilike(f'%{value}%'))
        value = query_params.get('isUnique', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.isUnique.ilike(f'%{value}%'))
        value = query_params.get('dropdownSource', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.dropdownSource.ilike(f'%{value}%'))
        value = query_params.get('desktopWidth', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.desktopWidth.ilike(f'%{value}%'))
        value = query_params.get('mobileWidth', '').strip()
        if isinstance(value, str) and len(value) > 0:
            query = query.filter(Model.mobileWidth.ilike(f'%{value}%'))

        return query

    async def create(self, db: Session, model_request):
        required_fields = ['model_builder_id', 'name', 'type', 'label', 'dataType', 'defaultValue', 'isVisibleInList', 'isVisibleInSingleView', 'isRequired', 'isUnique', 'desktopWidth', 'mobileWidth']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
        current_time = datetime.now()
        db_query = Model(
            created_at=current_time,
            updated_at=current_time,
            model_builder_id=model_request.model_builder_id,
            name=model_request.name,
            type=model_request.type,
            label=model_request.label,
            dataType=model_request.dataType,
            defaultValue=model_request.defaultValue,
            isVisibleInList=model_request.isVisibleInList,
            isVisibleInSingleView=model_request.isVisibleInSingleView,
            isRequired=model_request.isRequired,
            isUnique=model_request.isUnique,
            dropdownSource=model_request.dropdownSource,
            dropdownDependsOn=model_request.dropdownDependsOn,
            desktopWidth=model_request.desktopWidth,
            mobileWidth=model_request.mobileWidth,
        )
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
        required_fields = ['model_builder_id', 'name', 'type', 'label', 'dataType', 'defaultValue', 'isVisibleInList', 'isVisibleInSingleView', 'isRequired', 'isUnique', 'desktopWidth', 'mobileWidth']
        unique_fields = []
        Validator.validate_required_fields(model_request, required_fields)
        UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db_query.updated_at = current_time
            db_query.model_builder_id = model_request.model_builder_id
            db_query.name = model_request.name
            db_query.type = model_request.type
            db_query.label = model_request.label
            db_query.dataType = model_request.dataType
            db_query.defaultValue = model_request.defaultValue
            db_query.isVisibleInList = model_request.isVisibleInList
            db_query.isVisibleInSingleView = model_request.isVisibleInSingleView
            db_query.isRequired = model_request.isRequired
            db_query.isUnique = model_request.isUnique
            db_query.dropdownSource = model_request.dropdownSource
            db_query.dropdownDependsOn = model_request.dropdownDependsOn
            db_query.desktopWidth = model_request.desktopWidth
            db_query.mobileWidth = model_request.mobileWidth
            db.commit()
            db.refresh(db_query)
            await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')
            return db_query
        else:
            return ResponseHelper.handle_not_found_error(model_id)
