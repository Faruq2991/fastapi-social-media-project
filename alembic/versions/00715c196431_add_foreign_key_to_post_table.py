"""add foreign key to post table.

Revision ID: 00715c196431
Revises: ee8272f257bf
Create Date: 2025-05-09 17:54:50.928474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00715c196431'
down_revision: Union[str, None] = 'ee8272f257bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_foreign_key(
        'fk_user_id',
        'posts',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE'
    )
    pass


def downgrade():
    """Downgrade schema."""
    op.drop_constraint('fk_user_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
    pass
