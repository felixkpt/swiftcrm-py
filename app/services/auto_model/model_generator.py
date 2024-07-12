import os
import subprocess
from app.services.auto_model.saves_file import handler
from app.repositories.auto_page_builder_repo import AutoPageBuilderRepo as Repo
from app.services.auto_model.helpers import generate_model_and_api_names
from sqlalchemy.orm import Session


class ModelGenerator:
    def __init__(self, data, db: Session):
        """
        Initializes the ModelGenerator instance with input data.

        Args:
            data (dict): Input data containing fields, class_name, table_name, options, etc.
        """
        
        self.data = data
        if 'options' not in self.data:
            self.data['options'] = {}
        if 'timestamps' not in self.data['options']:
            self.data['options']['timestamps'] = True

        self.db = db
        self.type_mapping = {
            'string': {'name': 'String', 'length': 255},
            'integer': {'name': 'Integer', 'length': None},
            'text': {'name': 'Text', 'length': None},
            'longtext': {'name': 'Text', 'length': None},
            'json': {'name': 'JSON', 'length': None},
        }

    def _generate_fields(self):
        """
        Generates a list of fields based on input data.

        Returns:
            list: List of dictionaries representing each field.
        """
        fields = self.data['fields']
        print('Fields:', fields)
        return [
            {
                "name": field.name,
                "type": field.type,
                "label": field.label,
                "isRequired": field.isRequired,
                "dataType": field.dataType,
                "defaultValue": field.defaultValue,
                "isUnique": field.isUnique,
                "dropdownSource": field.dropdownSource,
                "isPrimaryKey": False,
                "autoIncrements": False,
            }
            for field in fields
        ]

    def _add_id_field(self, fields):
        """
        Adds an 'id' field if not present in the list of fields.

        Args:
            fields (list): List of dictionaries representing fields.

        Returns:
            list: Updated list of fields including 'id' field.
        """
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
        """
        Filters out fields to ignore (e.g., 'created_at', 'updated_at').

        Args:
            fields (list): List of dictionaries representing fields.

        Returns:
            list: Filtered list of fields.
        """
        ignore_fields = ['created_at', 'updated_at']
        return [field for field in fields if 'name' not in field or field['name'] not in ignore_fields]

    def _collect_imports(self, fields):
        """
        Collects necessary imports based on field types.

        Args:
            fields (list): List of dictionaries representing fields.

        Returns:
            str: Comma-separated string of imports.
        """
        imports = set()
        for field in fields:
            print('HEY YOU:::', field.get('dropdownSource', False))

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
        relationships = []
        for field in fields:
            if field.get('dropdownSource'):
                rship_tbl_name = field['dropdownSource']
                auto_page = Repo.get_page_by_table_name(
                    self.db, rship_tbl_name)
                if auto_page:
                    generated_data = generate_model_and_api_names(auto_page)
                    model_name_singular = generated_data['model_name_singular']
                    class_name = generated_data['class_name']
                    back_populates = self.data['model_name_singular'].lower()

                    relationship_str = f'    {model_name_singular.lower()} = relationship("{class_name}", back_populates="{back_populates}")'
                    relationships.append(relationship_str)
        return '\n'.join(relationships) if relationships else ''

    def _build_model_content(self, imports_str, fields):
        """
        Builds the content of the SQLAlchemy model class.

        Args:
            imports_str (str): Comma-separated string of imports.
            fields (list): List of dictionaries representing fields.

        Returns:
            str: Content of the SQLAlchemy model class.
        """
        content = (
            f"from sqlalchemy import Column, {imports_str}\n"
            "from app.models.base import Base\n"
            "from sqlalchemy.orm import relationship\n\n"
            f"class {self.data['class_name']}(Base):\n"
            f"    __tablename__ = '{self.data['table_name']}'\n"
        )
        for field in fields:
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
                    column_args += f", ForeignKey('{field['dropdownSource']}.id')"

                content += f"    {field['name']} = Column({column_type_name}{column_args})\n"
            else:
                if field.get('isPrimaryKey', False):
                    column_args += ", primary_key=True"
                if field.get('isUnique', False):
                    column_args += ", unique=True"
                content += f"    {field['name']} = Column({column_type_name}{column_args})\n"
        content += "    status_id = Column(Integer, nullable=False, server_default='1')\n"
        if self.data.get('options') and self.data['options'].get('timestamps'):
            content += "    created_at = Column(DateTime, server_default=func.now())\n"
            content += "    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())\n"
        # Adding relationships
        rels = self._add_relationships(fields)
        if rels:
            content += '\n'+rels

        return content

    def _write_model_file(self, content):
        """
        Writes the SQLAlchemy model file to the specified directory.

        Args:
            content (str): Content of the SQLAlchemy model class.
        """
        path = self.data['api_endpoint'].replace('-', '_')
        filename = f"{self.data['model_name_singular'].lower()}.py"
        directory_path = handler(path, 'models', filename, content)
        init_py_path = os.path.join(directory_path, '__init__.py')
        with open(init_py_path, 'a') as init_py:
            if not content.endswith('\n'):
                init_py.write('\n')

    def generate_model(self):
        """
        Generates the SQLAlchemy model and performs database migrations using Alembic.

        Returns:
            bool: True if successful, False otherwise.
        """
        fields = self._generate_fields()
        fields = self._add_id_field(fields)
        fields = self._filter_ignore_fields(fields)
        imports_str = self._collect_imports(fields)
        content = self._build_model_content(imports_str, fields)
        self._write_model_file(content)
        try:
            subprocess.run(['alembic', 'revision', '--autogenerate', '-m',
                            f"Added: {self.data['api_endpoint'].replace('/', ' > ')+' '+self.data['model_name_singular'].lower()} table"], check=True)
            subprocess.run(['alembic', 'upgrade', 'head'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error running Alembic commands: {e}")
            return False
