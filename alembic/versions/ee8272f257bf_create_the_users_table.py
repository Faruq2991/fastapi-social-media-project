"""Create the users table.

Revision ID: ee8272f257bf
Revises: cae5e9c770b1
Create Date: 2025-05-09 17:49:34.737366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee8272f257bf'
down_revision: Union[str, None] = 'cae5e9c770b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='TRUE', nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default='FALSE', nullable=False),
        sa.Column('is_admin', sa.Boolean(), server_default='FALSE', nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    pass


def downgrade():
    """Downgrade schema."""
    op.drop_table('users')
    pass
