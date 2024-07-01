from sqlalchemy import ForeignKey, BIGINT
from src.infrastructure.databases import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


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


class GroupsVsPermissions(BaseModel):
    """
    Relacionamento NxM entre grupos e permissões.
    """

    __tablename__ = "groups_vs_permissions"

    group_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('groups.id'), primary_key=True)
    permission_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('permissions.id'), primary_key=True)
