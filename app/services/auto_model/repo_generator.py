import os

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def generate_repo(model_name, model_name_pluralized, fields):
    model_path_name = model_name.lower()
    content = f"""
from sqlalchemy.orm import Session
from app.models.{model_path_name} import {model_name}

class {model_name}Repo:

    @staticmethod
    def list_{model_name_pluralized.lower()}(db: Session, skip: int = 0, limit: int = 10):
        return db.query({model_name}).offset(skip).limit(limit).all()

    @staticmethod
    def get_{model_name.lower()}(db: Session, {model_name.lower()}_id: int):
        return db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()

    @staticmethod
    def create_{model_name.lower()}(db: Session, {model_name.lower()}):
        current_time = datetime.now()
        db_{model_name.lower()} = {model_name}(
"""

    for field in fields:
        if field['name'] == 'created_at' or field['name'] == 'updated_at':
            content += f"            {field['name']}=current_time,\n"
        elif field['name'] != 'id':
            content += f"            {field['name']}={model_name.lower()}.{field['name']},\n"

    content += f"""        )
        db.add(db_{model_name.lower()})
        db.commit()
        db.refresh(db_{model_name.lower()})
        return db_{model_name.lower()}

    @staticmethod
    def update_{model_name.lower()}(db: Session, {model_name.lower()}_id: int, {model_name.lower()}):
        current_time = datetime.now()
        db_{model_name.lower()} = db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()
        if db_{model_name.lower()}:
"""

    for field in fields:
        if field['name'] == 'updated_at':
            content += f"            db_{model_name.lower()}.{field['name']} = current_time\n"
        elif field['name'] != 'id' and field['name'] != 'created_at':
            content += f"            db_{model_name.lower()}.{field['name']} = {model_name.lower()}.{field['name']}\n"

    content += f"""        db.commit()
        db.refresh(db_{model_name.lower()})
        return db_{model_name.lower()}

    @staticmethod
    def delete_{model_name.lower()}(db: Session, {model_name.lower()}_id: int):
        db_{model_name.lower()} = db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()
        if db_{model_name.lower()}:
            db.delete(db_{model_name.lower()})
            db.commit()
            return True
        return False
"""

    # Ensure the models directory exists
    directory_path = os.path.join(os.getcwd(), 'app', 'repositories')
    create_directory_if_not_exists(directory_path)

    # Write the generated repo content to a Python file
    model_filename = f'{model_name.lower()}_repo.py'
    model_filepath = os.path.join(directory_path, model_filename)
    with open(model_filepath, 'w') as f:
        f.write(content)

    return True
