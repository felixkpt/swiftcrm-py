"""initial migration

Revision ID: 7ba871276f1d
Revises: 
Create Date: 2024-06-22 02:37:12.239352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ba871276f1d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auto_page_builder',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('modelName', sa.String(length=255), nullable=False),
    sa.Column('modelURI', sa.String(length=255), nullable=False),
    sa.Column('apiEndpoint', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auto_page_builder_action_labels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('auto_page_builder_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('actionType', sa.String(length=50), nullable=False),
    sa.Column('show', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['auto_page_builder_id'], ['auto_page_builder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auto_page_builder_fields',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('auto_page_builder_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('isRequired', sa.Integer(), nullable=False),
    sa.Column('dataType', sa.String(length=50), nullable=True),
    sa.Column('defaultValue', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['auto_page_builder_id'], ['auto_page_builder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auto_page_builder_headers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('auto_page_builder_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('isVisibleInList', sa.Integer(), nullable=False),
    sa.Column('isVisibleInSingleView', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['auto_page_builder_id'], ['auto_page_builder.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auto_page_builder_headers')
    op.drop_table('auto_page_builder_fields')
    op.drop_table('auto_page_builder_action_labels')
    op.drop_table('auto_page_builder')
    # ### end Alembic commands ###
