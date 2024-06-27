from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel
from .many_to_many import users_vs_permissions, groups_vs_permissions


class Permission(BaseModel):
    """
    Classe de permissões de usuários e/ou grupos.
    """

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

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
