import os
import subprocess
from app.modules.auto_builders.model_builder.services.saves_file import handler, generate_file_path
from sqlalchemy.orm import Session


class ModelGenerator:
    def __init__(self, data, db: Session):
        from app.modules.auto_builders.model_builder.model_builder_repo import ModelBuilderRepo as Repo 
        self.repo = Repo

        data['nameSingular'] = data['nameSingular'].replace('-', '_')
        data['namePlural'] = data['namePlural'].replace('-', '_')

        self.data = data
        if 'options' not in self.data:
            self.data['options'] = {}
        if 'timestamps' not in self.data['options']:
            self.data['options']['timestamps'] = True
        if 'user_id' not in self.data['options']:
            self.data['options']['user_id'] = True

        self.db = db
        self.type_mapping = {
            'string': {'name': 'String', 'length': 255},
            'integer': {'name': 'Integer', 'length': None},
            'boolean': {'name': 'Integer', 'length': 1},
            'text': {'name': 'Text', 'length': None},
            'longtext': {'name': 'Text', 'length': None},
            'json': {'name': 'JSON', 'length': None},
        }

    def _add_id_field(self, fields):
        id_field = next(
            (field for field in fields if field['name'] == 'id'), None)
        if id_field is None:
            fields.insert(0, {
                "name": "id",
                "type": "integer",
                "label": "id",
                "dataType": "integer",
                "isPrimaryKey": True,
                "autoIncrements": True,
                "isRequired": False,
                "defaultValue": None,
                "hidden": True
            })
        else:
            id_field.update({
                "dataType": id_field['dataType'] or 'integer',
                "isPrimaryKey": True,
                "autoIncrements": True
            })
        return fields

    def _filter_ignore_fields(self, fields):
        ignore_fields = ['created_at', 'updated_at']
        return [field for field in fields if 'name' not in field or field['name'] not in ignore_fields]

    def _collect_imports(self, fields):
        imports = set()
        for field in fields:

            data_type = field['dataType'].lower() if field['dataType'] else ''
            if data_type in self.type_mapping:
                imports.add(self.type_mapping[data_type]['name'])
            else:
                imports.add('String')
            if field.get('dropdownSource', False):
                imports.add('ForeignKey')

        if self.data.get('options') and self.data['options'].get('timestamps'):
            imports.add('DateTime')
            imports.add('func')

        return ', '.join(sorted(imports))

    def _add_relationships(self, fields):
        from app.modules.auto_builders.model_builder.services.helpers import generate_model_and_api_names

        relationships = []
        for field in fields:
            if field.get('dropdownSource'):
                rship_tbl_name = field['dropdownSource']
                auto_page = self.repo.get_page_by_tableName(
                    self.db, rship_tbl_name)
                if auto_page:
                    generated_data = generate_model_and_api_names(auto_page)
                    nameSingular = generated_data['nameSingular'].replace('-', '_')
                    className = generated_data['className']
                    # back_populates = self.data['nameSingular'].lower()
                    back_populates = None

                    relationship_str = f'    {nameSingular.lower()} = relationship("{className}", back_populates={back_populates})'
                    relationships.append(relationship_str)
        return '\n'.join(relationships) if relationships else ''

    def _extract_existing_relationships(self, file_path):
        relationships = []

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if 'relationship(' in line:
                        relationships.append(line.strip())
        return relationships

    def _build_model_content(self, imports_str, fields, existing_relationships):
        content = (
            f"from sqlalchemy import Column, ForeignKey, {imports_str}\n"
            "from app.models.base import Base\n"
            "from sqlalchemy.orm import relationship\n\n"
            f"class {self.data['className']}(Base):\n"
            f"    __tablename__ = '{self.data['tableNamePlural']}'\n"
        )
        
        for field in fields:
            if field.get('name', False) == 'user_id': continue

            data_type = field['dataType'].lower() if field['dataType'] else ''
            sqlalchemy_type = self.type_mapping.get(
                data_type, {'name': 'String'})
            column_type_name = sqlalchemy_type['name']
            column_args = f"({sqlalchemy_type['length']})" if 'length' in sqlalchemy_type else '(255)' if column_type_name == 'String' else ''
            if column_type_name == 'Integer':
                column_args = ''
                if field.get('isPrimaryKey', False):
                    column_args += ", primary_key=True"
                    if field.get('autoIncrements', False):
                        column_args += ", autoincrement=True"
                if field.get('isUnique', False):
                    column_args += ", unique=True"
                if field.get('dropdownSource', False):
                    auto_page = self.repo.get_page_by_apiEndpoint(
                        self.db, field['dropdownSource'])
                    if auto_page:
                        column_args += f", ForeignKey('{auto_page.tableNamePlural}.id')"

                content += f"    {field['name']} = Column({column_type_name}{column_args})\n"
            else:
                if field.get('isPrimaryKey', False):
                    column_args += ", primary_key=True"
                if field.get('isUnique', False):
                    column_args += ", unique=True"
                content += f"    {field['name']} = Column({column_type_name}{column_args})\n"
        
        if self.data.get('options'):
            content += "    user_id = Column(Integer, ForeignKey('users.id'))\n"
        content += "    status_id = Column(Integer, nullable=False, server_default='1')\n"
        if self.data.get('options') and self.data['options'].get('timestamps'):
            content += "    created_at = Column(DateTime, server_default=func.now())\n"
            content += "    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())\n"
        
        # Adding existing relationships
        if existing_relationships:
            content += '\n' + \
                '\n'.join(
                    f"    {line}" for line in existing_relationships) + '\n'

        print('existing_relationships,', existing_relationships)
        return content

    def _write_model_file(self, content):
        path = self.data['api_endpoint'].replace('-', '_')
        filename = f"{self.data['nameSingular'].lower()}_model.py"
        directory_path = handler(path, 'modules', filename, content)
        init_py_path = os.path.join(directory_path, '__init__.py')
        with open(init_py_path, 'a') as init_py:
            if not content.endswith('\n'):
                init_py.write('\n')

    def generate_model(self):

        fields = self.data['fields']
        fields = self._add_id_field(fields)
        fields = self._filter_ignore_fields(fields)
        imports_str = self._collect_imports(fields)

        # Get existing relationships
        path = self.data['api_endpoint'].replace('-', '_')
        filename = f"{self.data['nameSingular'].lower()}_model.py"
        res = generate_file_path(path, 'modules', filename)
        file_path = res['file_path']

        existing_relationships = self._extract_existing_relationships(
            file_path)

        content = self._build_model_content(
            imports_str, fields, existing_relationships)
        self._write_model_file(content)
        try:
            subprocess.run(['alembic', 'revision', '--autogenerate', '-m',
                            f"Added: {self.data['api_endpoint'].replace('/', ' > ')+' '+self.data['nameSingular'].lower()} table"], check=True)
            subprocess.run(['alembic', 'upgrade', 'head'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running Alembic commands: {e}")
            return False
