import os
from app.services.helpers import get_model_names

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_repo(model_name, fields):
    model_name_singular, model_name_plural, model_name_pascal = get_model_names(model_name)

    model_path_name = model_name_singular.lower()
    content = f"""
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.{model_path_name} import {model_name_pascal} as Model

class {model_name_pascal}Repo:

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Model).offset(skip).limit(limit).all()

    @staticmethod
    def get(db: Session, model_id: int):
        return db.query(Model).filter(Model.id == model_id).first()

    @staticmethod
    def create(db: Session, model_request):
"""

    # Add validation for unique fields
    for field in fields:
        if field.isUnique:
            content += f"""
        # Validate unique {field.name}
        existing_{field.name} = db.query(Model).filter(Model.{field.name} == model_request.{field.name}).first()
        if existing_{field.name}:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A record with this {field.name} already exists."
            )
"""

    content += """
        current_time = datetime.now()
        db_query = Model(
"""

    for field in fields:
        if field.name == 'created_at' or field.name == 'updated_at':
            content += f"            {field.name}=current_time,\n"
        elif field.name != 'id':
            content += f"            {field.name}=model_request.{field.name},\n"

    content += """        )
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
        current_time = datetime.now()
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
"""

    # Add validation for unique fields during update
    for field in fields:
        if field.isUnique:
            content += f"""
            # Validate unique {field.name} during update
            existing_{field.name} = db.query(Model).filter(Model.{field.name} == model_request.{field.name}, Model.id != model_id).first()
            if existing_{field.name}:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A record with this {field.name} already exists."
                )
"""

    for field in fields:
        if field.name == 'updated_at':
            content += f"            db_query.{field.name} = current_time\n"
        elif field.name != 'id' and field.name != 'created_at':
            content += f"            db_query.{field.name} = model_request.{field.name}\n"

    content += """        db.commit()
        db.refresh(db_query)
        return db_query

    @staticmethod
    def delete(db: Session, model_id: int):
        db_query = db.query(Model).filter(Model.id == model_id).first()
        if db_query:
            db.delete(db_query)
            db.commit()
            return True
        return False
"""

    # Ensure the repositories directory exists
    directory_path = os.path.join(os.getcwd(), 'app', 'repositories')
    create_directory_if_not_exists(directory_path)

    # Write the generated repo content to a Python file
    model_filename = f'{model_name_singular.lower()}_repo.py'
    model_filepath = os.path.join(directory_path, model_filename)
    with open(model_filepath, 'w') as f:
        f.write(content)

    return True
