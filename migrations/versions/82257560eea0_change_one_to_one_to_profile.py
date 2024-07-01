"""change_one_to_one_to_profile

Revision ID: 82257560eea0
Revises: 7d6dc6f4751f
Create Date: 2024-07-01 23:27:30.700925

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82257560eea0'
down_revision: Union[str, None] = '7d6dc6f4751f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('groups_vs_permissions', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('groups_vs_permissions', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('groups_vs_permissions', sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False))
    op.alter_column('groups_vs_permissions', 'group_id', existing_type=sa.BIGINT(), nullable=False)
    op.alter_column('groups_vs_permissions', 'permission_id', existing_type=sa.BIGINT(), nullable=False)
    op.create_index(op.f('ix_groups_vs_permissions_created_at'), 'groups_vs_permissions', ['created_at'], unique=False)
    op.create_index(op.f('ix_groups_vs_permissions_is_deleted'), 'groups_vs_permissions', ['is_deleted'], unique=False)
    op.add_column('profiles', sa.Column('user_id', sa.BIGINT(), nullable=False))
    op.create_foreign_key(None, 'profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('users_profile_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'profile_id')
    op.add_column('users_vs_groups', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users_vs_groups', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users_vs_groups', sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False))
    op.alter_column('users_vs_groups', 'user_id', existing_type=sa.BIGINT(), nullable=False)
    op.alter_column('users_vs_groups', 'group_id', existing_type=sa.BIGINT(), nullable=False)
    op.create_index(op.f('ix_users_vs_groups_created_at'), 'users_vs_groups', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_vs_groups_is_deleted'), 'users_vs_groups', ['is_deleted'], unique=False)
    op.add_column('users_vs_permissions', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users_vs_permissions', sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False))
    op.add_column('users_vs_permissions', sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False))
    op.alter_column('users_vs_permissions', 'user_id', existing_type=sa.BIGINT(), nullable=False)
    op.alter_column('users_vs_permissions', 'permission_id', existing_type=sa.BIGINT(), nullable=False)
    op.create_index(op.f('ix_users_vs_permissions_created_at'), 'users_vs_permissions', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_vs_permissions_is_deleted'), 'users_vs_permissions', ['is_deleted'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_vs_permissions_is_deleted'), table_name='users_vs_permissions')
    op.drop_index(op.f('ix_users_vs_permissions_created_at'), table_name='users_vs_permissions')
    op.alter_column('users_vs_permissions', 'permission_id', existing_type=sa.BIGINT(), nullable=True)
    op.alter_column('users_vs_permissions', 'user_id', existing_type=sa.BIGINT(), nullable=True)
    op.drop_column('users_vs_permissions', 'is_deleted')
    op.drop_column('users_vs_permissions', 'updated_at')
    op.drop_column('users_vs_permissions', 'created_at')
    op.drop_index(op.f('ix_users_vs_groups_is_deleted'), table_name='users_vs_groups')
    op.drop_index(op.f('ix_users_vs_groups_created_at'), table_name='users_vs_groups')
    op.alter_column('users_vs_groups', 'group_id', existing_type=sa.BIGINT(), nullable=True)
    op.alter_column('users_vs_groups', 'user_id', existing_type=sa.BIGINT(), nullable=True)
    op.drop_column('users_vs_groups', 'is_deleted')
    op.drop_column('users_vs_groups', 'updated_at')
    op.drop_column('users_vs_groups', 'created_at')
    op.add_column('users', sa.Column('profile_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.create_foreign_key('users_profile_id_fkey', 'users', 'profiles', ['profile_id'], ['id'])
    op.drop_constraint(None, 'profiles', type_='foreignkey')
    op.drop_column('profiles', 'user_id')
    op.drop_index(op.f('ix_groups_vs_permissions_is_deleted'), table_name='groups_vs_permissions')
    op.drop_index(op.f('ix_groups_vs_permissions_created_at'), table_name='groups_vs_permissions')
    op.alter_column('groups_vs_permissions', 'permission_id', existing_type=sa.BIGINT(), nullable=True)
    op.alter_column('groups_vs_permissions', 'group_id', existing_type=sa.BIGINT(), nullable=True)
    op.drop_column('groups_vs_permissions', 'is_deleted')
    op.drop_column('groups_vs_permissions', 'updated_at')
    op.drop_column('groups_vs_permissions', 'created_at')
