# app/services/auto_model/crud_generator.py
import os


def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def generate_crud(model_name, model_name_pluralized, fields):
    content = f"""
def list_{model_name_pluralized.lower()}(db, skip=0, limit=10):
    return db.query({model_name}).offset(skip).limit(limit).all()


def get_{model_name.lower()}(db, {model_name.lower()}_id):
    return db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()


def create_{model_name.lower()}(db, {model_name.lower()}):
    current_time = datetime.now()
    db_{model_name.lower()} = {model_name}(
"""

    for field in fields:
        if field['name'] == 'created_at' or field['name'] == 'updated_at':
            content += f"        {field['name']}=current_time,\n"
        elif field['name'] != 'id':
            content += f"        {field['name']}={model_name.lower()}.{field['name']},\n"

    content += f"""    )
    db.add(db_{model_name.lower()})
    db.commit()
    db.refresh(db_{model_name.lower()})
    return db_{model_name.lower()}


def update_{model_name.lower()}(db, {model_name.lower()}_id, {model_name.lower()}):
    current_time = datetime.now()
    db_{model_name.lower()} = db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()
    if db_{model_name.lower()}:
"""

    for field in fields:
        if field['name'] == 'updated_at':
            content += f"        db_{model_name.lower()}.{field['name']} = current_time\n"
        elif field['name'] != 'id' and field['name'] != 'created_at':
            content += f"        db_{model_name.lower()}.{field['name']} = {model_name.lower()}.{field['name']}\n"

    content += f"""    db.commit()
    db.refresh(db_{model_name.lower()})
    return db_{model_name.lower()}


def delete_{model_name.lower()}(db, {model_name.lower()}_id):
    db_{model_name.lower()} = db.query({model_name}).filter({model_name}.id == {model_name.lower()}_id).first()
    if db_{model_name.lower()}:
        db.delete(db_{model_name.lower()})
        db.commit()
        return True
    return False
"""

    return content
