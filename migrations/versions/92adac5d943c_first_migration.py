"""
first_migration

Revision ID: 92adac5d943c
Revises:
Create Date: 2024-06-28 00:36:44.015631
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92adac5d943c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Gerando todas as tabelas.
    """

    op.create_table(
        'profiles',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('phone', sa.VARCHAR(length=11), nullable=True),
        sa.Column('address', sa.VARCHAR(length=100), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profiles_created_at'), 'profiles', ['created_at'], unique=False)
    op.create_index(op.f('ix_profiles_is_deleted'), 'profiles', ['is_deleted'], unique=False)

    op.create_table(
        'users',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('email', sa.VARCHAR(length=50), nullable=False),
        sa.Column('password', sa.VARCHAR(length=30), nullable=False),
        sa.Column('name', sa.VARCHAR(length=30), nullable=False),
        sa.Column('profile_id', sa.BIGINT(), nullable=False),
        sa.Column('work_company_cnpj', sa.VARCHAR(length=14), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_is_deleted'), 'users', ['is_deleted'], unique=False)

    op.create_table(
        'companies',
        sa.Column('cnpj', sa.VARCHAR(length=14), nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('fantasy_name', sa.VARCHAR(length=50), nullable=True),
        sa.Column('owner_id', sa.BIGINT(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='fk_company_owner', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('cnpj')
    )
    op.create_index(op.f('ix_companies_created_at'), 'companies', ['created_at'], unique=False)
    op.create_index(op.f('ix_companies_is_deleted'), 'companies', ['is_deleted'], unique=False)

    op.create_table(
        'groups',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_created_at'), 'groups', ['created_at'], unique=False)
    op.create_index(op.f('ix_groups_is_deleted'), 'groups', ['is_deleted'], unique=False)

    op.create_table(
        'permissions',
        sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), nullable=False),
        sa.Column('code', sa.VARCHAR(length=20), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.BOOLEAN(), server_default=sa.text('false'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_created_at'), 'permissions', ['created_at'], unique=False)
    op.create_index(op.f('ix_permissions_is_deleted'), 'permissions', ['is_deleted'], unique=False)

    op.create_table(
        'groups_vs_permissions',
        sa.Column('group_id', sa.BIGINT(), nullable=True),
        sa.Column('permission_id', sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], )
    )

    op.create_table(
        'users_vs_groups',
        sa.Column('user_id', sa.BIGINT(), nullable=True),
        sa.Column('group_id', sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )

    op.create_table(
        'users_vs_permissions',
        sa.Column('user_id', sa.BIGINT(), nullable=True),
        sa.Column('permission_id', sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )


def downgrade() -> None:
    """
    Removendo todas as tabelas
    """

    op.drop_table('users_vs_permissions')
    op.drop_table('users_vs_groups')
    op.drop_table('groups_vs_permissions')
    op.drop_index(op.f('ix_users_is_deleted'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_profiles_is_deleted'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_created_at'), table_name='profiles')
    op.drop_table('profiles')
    op.drop_index(op.f('ix_permissions_is_deleted'), table_name='permissions')
    op.drop_index(op.f('ix_permissions_created_at'), table_name='permissions')
    op.drop_table('permissions')
    op.drop_index(op.f('ix_groups_is_deleted'), table_name='groups')
    op.drop_index(op.f('ix_groups_created_at'), table_name='groups')
    op.drop_table('groups')
    op.drop_index(op.f('ix_companies_is_deleted'), table_name='companies')
    op.drop_index(op.f('ix_companies_created_at'), table_name='companies')
    op.drop_table('companies')
