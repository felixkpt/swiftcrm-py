# app/services/auto_model/generate_crud.py
import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_crud(model_name, fields):
    model_name = model_name.capitalize()
    content = f"""from sqlalchemy.orm import Session
from app.models.{model_name.lower()} import {model_name}
from app.requests.schemas.{model_name.lower()} import {model_name}Schema


def get_{model_name.lower()}(db: Session, {model_name.lower()}_id: int):
    return db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()


def get_{model_name.lower()}(db: Session, skip: int = 0, limit: int = 10):
    return db.query({model_name}).offset(skip).limit(limit).all()


def create_{model_name.lower()}(db: Session, {model_name.lower()}: {model_name}Schema):
    db_{model_name.lower()} = {model_name}(
"""
    for field in fields:
        if field.name != 'id':
            content += f"        {field.name}={model_name.lower()}.{field.name},\n"
    
    content += f"""    )
    db.add(db_{model_name.lower()})
    db.commit()
    db.refresh(db_{model_name.lower()})
    return db_{model_name.lower()}
"""

    directory_path = os.path.join(os.getcwd(), 'app', 'database', 'crud')
    create_directory_if_not_exists(directory_path)
    with open(os.path.join(directory_path, f'{model_name.lower()}.py'), 'w') as f:
        f.write(content)
