"""Added: conversation > v3 > messages > word-confidences word_confidence table

Revision ID: a08db37b0c27
Revises: 662ebd239e9f
Create Date: 2024-07-21 11:04:06.926017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a08db37b0c27'
down_revision: Union[str, None] = '662ebd239e9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
