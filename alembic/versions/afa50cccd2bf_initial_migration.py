"""Initial migration

Revision ID: afa50cccd2bf
Revises: 
Create Date: 2025-04-17 07:42:12.748282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afa50cccd2bf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blacklist',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=255), nullable=True),
    sa.Column('alternate_phone', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('password_confirmation', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('auto_builders_model_builders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=255), nullable=True),
    sa.Column('modelDisplayName', sa.String(length=255), nullable=True),
    sa.Column('name_singular', sa.String(length=255), nullable=True),
    sa.Column('name_plural', sa.String(length=255), nullable=True),
    sa.Column('modelURI', sa.String(length=255), nullable=True),
    sa.Column('apiEndpoint', sa.String(length=255), nullable=True),
    sa.Column('table_name_singular', sa.String(length=255), nullable=True),
    sa.Column('table_name_plural', sa.String(length=255), nullable=True),
    sa.Column('class_name', sa.String(length=255), nullable=True),
    sa.Column('createFrontendViews', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('apiEndpoint'),
    sa.UniqueConstraint('modelURI'),
    sa.UniqueConstraint('table_name_plural'),
    sa.UniqueConstraint('table_name_singular'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('refresh_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('refresh_token')
    )
    op.create_table('auto_builders_model_builder_action_labels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_builder_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=True),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('actionType', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['model_builder_id'], ['auto_builders_model_builders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auto_builders_model_builder_model_fields',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_builder_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('type', sa.String(length=255), nullable=True),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('dataType', sa.String(length=255), nullable=True),
    sa.Column('defaultValue', sa.String(length=255), nullable=True),
    sa.Column('isVisibleInList', sa.Integer(), nullable=True),
    sa.Column('isVisibleInSingleView', sa.Integer(), nullable=True),
    sa.Column('isRequired', sa.Integer(), nullable=True),
    sa.Column('isUnique', sa.Integer(), nullable=True),
    sa.Column('dropdownSource', sa.String(length=255), nullable=True),
    sa.Column('dropdownDependsOn', sa.JSON(none_as_null=None), nullable=True),
    sa.Column('desktopWidth', sa.Integer(), nullable=True),
    sa.Column('mobileWidth', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['model_builder_id'], ['auto_builders_model_builders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auto_builders_model_builder_model_headers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_builder_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=True),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('isVisibleInList', sa.Integer(), nullable=True),
    sa.Column('isVisibleInSingleView', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['model_builder_id'], ['auto_builders_model_builders.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('auto_builders_model_builder_model_headers')
    op.drop_table('auto_builders_model_builder_model_fields')
    op.drop_table('auto_builders_model_builder_action_labels')
    op.drop_table('refresh_tokens')
    op.drop_table('auto_builders_model_builders')
    op.drop_table('users')
    op.drop_table('token_blacklist')
    # ### end Alembic commands ###
