from typing import Optional
from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel
from .many_to_many import (
    groups_vs_permissions,
    users_vs_groups
)


class Group(BaseModel):
    """
    Classe de grupos de usuários.
    """

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    users: Mapped[Optional[list["User"]]] = relationship(
        "User",
        secondary=users_vs_groups,
        back_populates="groups",
        lazy='dynamic'
    )

    permissions: Mapped[Optional[list["Permission"]]] = relationship(
        "Permission",
        secondary=groups_vs_permissions,
        back_populates="groups",
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Group: {self.name}>"
