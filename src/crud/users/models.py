from typing import Optional
from sqlalchemy import VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.engines.databases import BaseModel


class User(BaseModel):
    """
    Classe de usuários.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)

    work_company_cnpj: Mapped[Optional[str]] = mapped_column(
        VARCHAR(14),
        ForeignKey('companies.cnpj', name='fk_employee_company'),
        nullable=True
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<User: {self.name}>"


class Profile(BaseModel):
    """
    Classe de perfis de usuários.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(11), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)
    user_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Profile: {self.id}>"


class UsersVsGroups(BaseModel):
    """
    Relacionamento NxM entre usuários e grupos.
    """

    __tablename__ = "users_vs_groups"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('groups.id'), primary_key=True)


class UsersVsPermissions(BaseModel):
    """
    Relacionamento NxM entre usuários e permissões.
    """

    __tablename__ = "users_vs_permissions"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id'), primary_key=True)
    permission_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('permissions.id'), primary_key=True)
