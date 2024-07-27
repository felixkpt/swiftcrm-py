"""Added: social-media > conversation > interviews interview table

Revision ID: 914d48a9d1d2
Revises: 13b6505c5b61
Create Date: 2024-07-27 21:06:27.593573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '914d48a9d1d2'
down_revision: Union[str, None] = '13b6505c5b61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_media_conversation_interviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('sub_category_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('scores', sa.Integer(), nullable=True),
    sa.Column('max_scores', sa.Integer(), nullable=True),
    sa.Column('percentage_score', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['social_media_conversation_categories.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['soc4bversation_categories_sub_categories_questions.id'], ),
    sa.ForeignKeyConstraint(['sub_category_id'], ['soc7e_media_conversation_categories_sub_categories.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_media_conversation_interviews')
    # ### end Alembic commands ###
