"""update_table_user_roles

Revision ID: 606f0f4ed6d0
Revises: bb48b23e4212
Create Date: 2025-07-11 10:29:45.622286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '606f0f4ed6d0'
down_revision: Union[str, Sequence[str], None] = 'bb48b23e4212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
