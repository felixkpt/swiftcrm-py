"""Added: social-media > conversation > categories > sub-categories sub_category table

Revision ID: c434843cf0c9
Revises: 447fd604516c
Create Date: 2024-07-22 23:00:51.483895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c434843cf0c9'
down_revision: Union[str, None] = '447fd604516c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_media_conversation_categories_sub_categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('sub_category_id', sa.Integer(), nullable=True),
    sa.Column('learn_instructions', sa.Text(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_media_conversation_categories_sub_categories')
    # ### end Alembic commands ###
