"""Added: conversation > v3 > word-confidences word_confidence table

Revision ID: 5107f860775c
Revises: 1270b058e04f
Create Date: 2024-07-20 13:29:29.872191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5107f860775c'
down_revision: Union[str, None] = '1270b058e04f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversation_v3_word_confidences',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('word', sa.String(length=255), nullable=True),
    sa.Column('start_time_seconds', sa.Integer(), nullable=True),
    sa.Column('end_time_seconds', sa.Integer(), nullable=True),
    sa.Column('confidence', sa.String(length=255), nullable=True),
    sa.Column('status_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['conversation_v3_messages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conversation_v3_word_confidences')
    # ### end Alembic commands ###
