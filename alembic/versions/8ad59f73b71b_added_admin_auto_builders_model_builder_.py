"""Added: admin > auto-builders > model-builder > model-headers model_header table

Revision ID: 8ad59f73b71b
Revises: e520fe528166
Create Date: 2024-07-21 15:35:09.230755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ad59f73b71b'
down_revision: Union[str, None] = 'e520fe528166'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_auto_builders_model_builder_model_headers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('model_builder_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(length=255), nullable=True),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('isVisibleInList', sa.String(length=255), nullable=True),
    sa.Column('isVisibleInSingleView', sa.String(length=255), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['model_builder_id'], ['admin_auto_builders_model_builder_model_builders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admin_auto_builders_model_builder_model_headers')
    # ### end Alembic commands ###
