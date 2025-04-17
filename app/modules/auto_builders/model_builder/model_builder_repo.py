
from datetime import datetime
from sqlalchemy.orm import joinedload
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.auto_builders.model_builder.model_builder_model import AutoBuildersModelBuilder as Model
from app.requests.validators.base_validator import Validator, UniqueChecker
from app.repositories.search_repo import get_query_params, apply_common_filters, set_metadata
from app.requests.response.response_helper import ResponseHelper
from app.repositories.base_repo import BaseRepo
from app.events.notifications import NotificationService
from app.modules.auto_builders.model_builder.model_fields.model_field_repo import ModelFieldRepo
from app.modules.auto_builders.model_builder.model_headers.model_header_repo import ModelHeaderRepo
from app.modules.auto_builders.model_builder.action_labels.action_label_repo import ActionLabelRepo
from app.modules.auto_builders.model_builder.services.auto_model_handler import auto_model_handler
from app.modules.auto_builders.model_builder.services.helpers import generate_model_and_api_names
from app.auth import user # Import user function
import os
import subprocess

class ModelBuilderRepo(BaseRepo):

	model = Model
	notification = NotificationService()

	async def list(self, db: Session, request: Request):
		query_params = get_query_params(request)
		search_fields = ['modelDisplayName', 'modelURI', 'apiEndpoint', 'createFrontendViews']

		query = db.query(Model)
		query = apply_common_filters(query, Model, search_fields, query_params)
		query = self.repo_specific_filters(query, Model, query_params)
		metadata = set_metadata(query, query_params)

		# Get current user ID
		current_user_id = user(request).id
		query = query.filter(Model.user_id == current_user_id)

		skip = (query_params['page'] - 1) * query_params['per_page']
		query = query.offset(skip).limit(query_params['per_page'])

		results = {
			"records": query.all(),
			"metadata": metadata
		}

		return results

	def repo_specific_filters(self, query, Model, query_params):
		value = query_params.get('uuid', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.uuid.ilike(f'%{value}%'))
		value = query_params.get('modelDisplayName', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.modelDisplayName.ilike(f'%{value}%'))
		value = query_params.get('name_singular', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.name_singular.ilike(f'%{value}%'))
		value = query_params.get('name_plural', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.name_plural.ilike(f'%{value}%'))
		value = query_params.get('modelURI', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.modelURI.ilike(f'%{value}%'))
		value = query_params.get('apiEndpoint', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.apiEndpoint.ilike(f'%{value}%'))
		value = query_params.get('table_name_singular', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.table_name_singular.ilike(f'%{value}%'))
		value = query_params.get('table_name_plural', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.table_name_plural.ilike(f'%{value}%'))
		value = query_params.get('class_name', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.class_name.ilike(f'%{value}%'))
		value = query_params.get('createFrontendViews', '').strip()
		if isinstance(value, str) and len(value) > 0:
			query = query.filter(Model.createFrontendViews.ilike(f'%{value}%'))
		value = query_params.get('user_id', None)
		if value is not None and value.isdigit():
			query = query.filter(Model.user_id == int(value))

		return query

	async def create(self, db: Session, model_request):
		generated_data = self.prepare_data(model_request)
		await auto_model_handler(generated_data, db)
		model_request.name_singular = generated_data['name_singular']
		model_request.name_plural = generated_data['name_plural']
		model_request.class_name = generated_data['class_name']
		model_request.table_name_singular = generated_data['table_name_singular']
		model_request.table_name_plural = generated_data['table_name_plural']

		required_fields = ['modelDisplayName', 'modelURI', 'apiEndpoint', 'createFrontendViews']
		unique_fields = ['uuid', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural']

		Validator.validate_required_fields(model_request, required_fields)
		UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields)
		current_time = datetime.now()
		current_user_id = user().id
		db_query = Model(
			uuid = str(model_request.uuid).strip(),
			modelDisplayName = str(model_request.modelDisplayName).strip(),
			name_singular = str(model_request.name_singular).strip(),
			name_plural = str(model_request.name_plural).strip(),
			modelURI = str(model_request.modelURI).strip(),
			apiEndpoint = str(model_request.apiEndpoint).strip(),
			table_name_singular = str(model_request.table_name_singular).strip(),
			table_name_plural = str(model_request.table_name_plural).strip(),
			class_name = str(model_request.class_name).strip(),
			createFrontendViews = model_request.createFrontendViews,
			user_id = current_user_id,
			created_at = current_time,
			updated_at = current_time,
		)
		db.add(db_query)
		try:
			db.commit()

			db.refresh(db_query)
			# Store fields, headers, and action labels using their respective repositories
			created_fields = []
			for field in model_request.fields:
				field.model_builder_id = db_query.id
				created_field = await ModelFieldRepo().create(db, field)
				created_fields.append(created_field)

			created_headers = []
			for header in model_request.headers:
				header.model_builder_id = db_query.id
				created_header = await ModelHeaderRepo().create(db, header)
				created_headers.append(created_header)

			created_action_labels = []
			for action_label in model_request.actionLabels:
				action_label.model_builder_id = db_query.id
				created_action_label = await ActionLabelRepo().create(db, action_label)
				created_action_labels.append(created_action_label)

			await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was created!')
		except IntegrityError as e:
			db.rollback()
			return ResponseHelper.handle_integrity_error(e)
		db.refresh(db_query)
		return db_query


	async def update(self, db: Session, model_id: int, model_request):
		generated_data = self.prepare_data(model_request)
		await auto_model_handler(generated_data, db)
		model_request.name_singular = generated_data['name_singular']
		model_request.name_plural = generated_data['name_plural']
		model_request.class_name = generated_data['class_name']
		model_request.table_name_singular = generated_data['table_name_singular']
		model_request.table_name_plural = generated_data['table_name_plural']

		required_fields = ['modelDisplayName', 'modelURI', 'apiEndpoint', 'createFrontendViews']
		unique_fields = ['uuid', 'modelURI', 'apiEndpoint', 'table_name_singular', 'table_name_plural']
		Validator.validate_required_fields(model_request, required_fields)
		UniqueChecker.check_unique_fields(db, Model, model_request, unique_fields, model_id)
		current_time = datetime.now()
		current_user_id = user().id
		db_query = db.query(Model).filter(Model.id == model_id, Model.user_id == current_user_id).first()
		if db_query:
			db_query.uuid = str(model_request.uuid).strip()
			db_query.modelDisplayName = str(model_request.modelDisplayName).strip()
			db_query.name_singular = str(model_request.name_singular).strip()
			db_query.name_plural = str(model_request.name_plural).strip()
			db_query.modelURI = str(model_request.modelURI).strip()
			db_query.apiEndpoint = str(model_request.apiEndpoint).strip()
			db_query.table_name_singular = str(model_request.table_name_singular).strip()
			db_query.table_name_plural = str(model_request.table_name_plural).strip()
			db_query.class_name = str(model_request.class_name).strip()
			db_query.createFrontendViews = model_request.createFrontendViews
			db_query.user_id = current_user_id
			db_query.updated_at = current_time
			db.commit()
			db.refresh(db_query)


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


			await self.notification.notify_model_updated(db, Model.__tablename__, 'Record was updated!')

			# Convert the model to a dictionary
			model_data = {column.name: getattr(
				db_query, column.name) for column in db_query.__table__.columns}

			# Combine and return the updated model with its related objects
			combined_result = {
				**model_data,
				"fields": created_fields,
				"headers": created_headers,
				"action_labels": created_action_labels
			}
			return combined_result

		return ResponseHelper.handle_not_found_error(model_id)

	def get(self, db: Session, model_id: int):
		print('model_id, mod', model_id)
		return db.query(Model).options(
			joinedload(Model.fields),
			joinedload(Model.action_labels),
			joinedload(Model.headers)
		).filter(Model.id == model_id).first()

	def get_page_by_name(db: Session, name_singular: str):
		return db.query(Model).filter(Model.name_singular == name_singular).first()

	def get_page_by_table_name(db: Session, table_name_singular: str):
		return db.query(Model).filter(Model.table_name_singular == table_name_singular).first()

	def get_page_by_table_name_plural(db: Session, table_name_plural: str):
		return db.query(Model).filter(Model.table_name_plural == table_name_plural).first()

	def get_page_by_apiEndpoint(db: Session, apiEndpoint: str):
		return db.query(Model).filter(Model.apiEndpoint == apiEndpoint).first()

	def prepare_data(self, model_request):
		generated_data = generate_model_and_api_names(model_request)
		model_request.name_singular = generated_data['name_singular']
		model_request.name_plural = generated_data['name_plural']
		model_request.table_name_singular = generated_data['table_name_singular']
		model_request.table_name_plural = generated_data['table_name_plural']
		model_request.class_name = generated_data['class_name']
		return generated_data

	async def delete(self, db: Session, model_id: int):
		# Query to find the model by its ID
		model = db.query(Model).filter(Model.id == model_id).first()

		if not model:
			return {"error": "Model not found"}, 404

		# Perform any necessary cleanup before deletion (e.g., migrations or related data)
		await self.delete_model_migrations(model)

		# Delete the model record
		db.delete(model)
		db.commit()

		# Notify of the deletion event
		notification = NotificationService()
		notification.notify_model_updated(db, Model.__tablename__, 'Record was deleted!')

		return {"message": "Record deleted successfully"}, 204

	async def delete_model_migrations(self, model):
		print(f"Performing cleanup for migrations of {model.table_name_plural}")

		# Search for migration files that mention the model name
		migration_dir = 'alembic/versions/'
		files = os.listdir(migration_dir)
		print(f"Migration files in directory: {files}")

		for filename in files:
			if filename.endswith(".py") and model.table_name_plural in filename:
				print(f"Removing migration file: {filename}")
				os.remove(os.path.join(migration_dir, filename))

		if len(files) > 0: 
			try:
				subprocess.run(['alembic', 'revision', '--autogenerate', '-m',
					f"Cleanup model migrations: {model.apiEndpoint.replace('/', ' > ')+' '+model.table_name_singular.lower()} table"], check=True)
				subprocess.run(['alembic', 'upgrade', 'head'], check=True)
				return True
			except subprocess.CalledProcessError as e:
				print(f"Error running Alembic commands: {e}")
				return False

