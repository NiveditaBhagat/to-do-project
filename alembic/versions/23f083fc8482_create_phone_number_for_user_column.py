"""Create phone number for user column

Revision ID:  
Revises: 
Create Date: 2025-05-29 00:32:29.789708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23f083fc8482'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(),nullable=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
