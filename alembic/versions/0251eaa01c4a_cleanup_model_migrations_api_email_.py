"""Cleanup model migrations:  > api > email-providers api_email_providers_emailprovider table

Revision ID: 0251eaa01c4a
Revises: 402a587a8805
Create Date: 2025-04-17 09:36:36.932514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0251eaa01c4a'
down_revision: Union[str, None] = '402a587a8805'
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
