from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.databases.base import Base


class UserVsGroup(Base):
    """
    Relacionamento NxM de usuários e grupos.
    """

    __tablename__ = "users_vs_groups"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)


class UserVsPermission(Base):
    """
    Relacionamento NxM de usuários e permissões.
    """

    __tablename__ = "users_vs_permissions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)


class GroupVsPermission(Base):
    """
    Relacionamento NxM de grupos e permissões.
    """

    __tablename__ = "groups_vs_permissions"

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)
