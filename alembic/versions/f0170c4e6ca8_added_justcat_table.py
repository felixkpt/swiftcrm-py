"""added justcat table

Revision ID: f0170c4e6ca8
Revises: 7ad1d8f5e0ea
Create Date: 2024-07-07 16:31:02.627907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0170c4e6ca8'
down_revision: Union[str, None] = '7ad1d8f5e0ea'
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
