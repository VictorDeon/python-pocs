"""users_company_relashionship

Revision ID: c623e4a34c76
Revises: 92adac5d943c
Create Date: 2024-06-28 00:58:35.168791

"""
from typing import Sequence, Union
from alembic import op


revision: str = 'c623e4a34c76'
down_revision: Union[str, None] = '92adac5d943c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Inserindo a chave estrangeira de empresas na tabela de usuários.
    """

    op.create_foreign_key('fk_employee_company', 'users', 'companies', ['work_company_cnpj'], ['cnpj'])


def downgrade() -> None:
    """
    Removendo a chave estrangeira.
    """

    op.drop_constraint('fk_employee_company', 'users', type_='foreignkey')
