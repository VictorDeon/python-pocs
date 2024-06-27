from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, Boolean
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

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

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
