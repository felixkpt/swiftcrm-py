from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = '0b0c7a82e7d5'
down_revision: Union[str, None] = '73a88328971b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Get the current database connection
    bind = op.get_bind()
    inspector = inspect(bind)
    
    # Check if the 'Number_of_employees' column exists in the 'companies' table
    columns = [col["name"] for col in inspector.get_columns('companies')]
    if 'Number_of_employees' in columns:
        op.drop_column('companies', 'Number_of_employees')
    
    # Add the 'number_of_employees' column
    op.add_column('companies', sa.Column('number_of_employees', sa.Integer(), nullable=True))

def downgrade() -> None:
    # Get the current database connection
    bind = op.get_bind()
    inspector = inspect(bind)
    
    # Check if the 'number_of_employees' column exists in the 'companies' table
    columns = [col["name"] for col in inspector.get_columns('companies')]
    if 'number_of_employees' in columns:
        op.drop_column('companies', 'number_of_employees')
    
    # Add the 'Number_of_employees' column back in the downgrade step
    op.add_column('companies', sa.Column('Number_of_employees', mysql.INTEGER(), autoincrement=False, nullable=True))
