"""Added: conversation > v3 > interviews interview table

Revision ID: a18fcf74ec1d
Revises: 5406da3083b3
Create Date: 2024-07-20 13:55:27.665488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a18fcf74ec1d'
down_revision: Union[str, None] = '5406da3083b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conversation_v3_word_confidences')
    op.create_foreign_key(None, 'conversation_v3_interviews', 'admin_users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'conversation_v3_interviews', type_='foreignkey')
    op.create_table('conversation_v3_word_confidences',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('message_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('word', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('start_time_seconds', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('end_time_seconds', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('confidence', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('status_id', mysql.INTEGER(), server_default=sa.text("'1'"), autoincrement=False, nullable=False),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['message_id'], ['conversation_v3_messages.id'], name='conversation_v3_word_confidences_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
