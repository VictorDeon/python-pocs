from typing import Optional
from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel
from .many_to_many import users_vs_permissions, groups_vs_permissions


class Permission(BaseModel):
    """
    Classe de permissões de usuários e/ou grupos.
    """

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    code: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)

    users: Mapped[Optional[list["User"]]] = relationship(
        "User",
        secondary=users_vs_permissions,
        back_populates="permissions",
        lazy='dynamic'
    )

    groups: Mapped[Optional[list["Group"]]] = relationship(
        "Group",
        secondary=groups_vs_permissions,
        back_populates="permissions",
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Permission: {self.name}>"
