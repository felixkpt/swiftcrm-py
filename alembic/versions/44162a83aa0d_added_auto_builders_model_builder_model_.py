"""Added: auto-builders > model-builder model_builder table

Revision ID: 44162a83aa0d
Revises: 8e6e00c64d80
Create Date: 2024-07-25 20:49:46.847310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44162a83aa0d'
down_revision: Union[str, None] = '8e6e00c64d80'
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
