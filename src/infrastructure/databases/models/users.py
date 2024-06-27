from typing import Optional
from sqlalchemy import VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel
from .many_to_many import (
    users_vs_groups,
    users_vs_permissions
)


class User(BaseModel):
    """
    Classe de usuários.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)

    profile_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey('profiles.id'),
        nullable=False
    )
    profile: Mapped["Profile"] = relationship(
        "Profile",
        single_parent=True,
        cascade="all, delete-orphan",
        back_populates="user"
    )

    companies: Mapped[list["Company"]] = relationship(
        'Company',
        back_populates='owner',
        cascade="all, delete-orphan",
        foreign_keys='Company.owner_id'
    )

    work_company_cnpj: Mapped[Optional[str]] = mapped_column(
        VARCHAR(14),
        ForeignKey('companies.cnpj', name='fk_employee_company'),
        nullable=True
    )
    work_company = relationship(
        'Company',
        back_populates='employees',
        foreign_keys=[work_company_cnpj]
    )

    groups: Mapped[Optional[list["Group"]]] = relationship(
        "Group",
        secondary=users_vs_groups,
        back_populates="users",
        lazy='dynamic'
    )

    permissions: Mapped[Optional[list["Permission"]]] = relationship(
        "Permission",
        secondary=users_vs_permissions,
        back_populates="users",
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<User: {self.name}>"
