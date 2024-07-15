"""Added: dash > leads lead table

Revision ID: cb8ce1df3a0d
Revises: 7be8f3924cee
Create Date: 2024-07-15 13:55:30.032780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb8ce1df3a0d'
down_revision: Union[str, None] = '7be8f3924cee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dash_leads',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('dash_leads_categories_lead_category_id', sa.Integer(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['dash_leads_categories_lead_category_id'], ['dash_leads_categories_lead_categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dash_leads')
    # ### end Alembic commands ###
