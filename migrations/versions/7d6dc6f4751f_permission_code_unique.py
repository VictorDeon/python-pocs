"""permission_code_unique

Revision ID: 7d6dc6f4751f
Revises: c623e4a34c76
Create Date: 2024-06-30 22:44:55.335943

"""
from typing import Sequence, Union
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '7d6dc6f4751f'
down_revision: Union[str, None] = 'c623e4a34c76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'permissions', ['code'])


def downgrade() -> None:
    op.drop_constraint(None, 'permissions', type_='unique')
