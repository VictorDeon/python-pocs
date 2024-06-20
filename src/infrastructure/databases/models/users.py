from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.databases import BaseModel
from src.infrastructure.databases.models.__many_to_many import (
    user_group_many_to_many,
    user_permission_many_to_many
)
from .groups import Group
from .profiles import Profile
from .permissions import Permission


class User(BaseModel):
    """
    Classe de usuários.
    """

    __tablename__ = "users"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = Column(String(50), nullable=False, index=True, unique=True)
    password: Mapped[str] = Column(String(30), nullable=False)
    name: Mapped[str] = Column(String(30), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = Column(Boolean, default=False, index=True)

    profile_id: Mapped[int] = Column(BigInteger, ForeignKey('profiles.id'))
    profile: Mapped[Profile] = relationship(
        "Profile",
        uselist=False,
        backref='user'
    )

    companies = relationship(
        'Company',
        back_populates='owner',
        foreign_keys='Company.owner_id'
    )

    work_company_cnpj: Mapped[str] = Column(String(14), ForeignKey('companies.cnpj', name='fk_employee_company'))
    work_company = relationship(
        'Company',
        back_populates='employees',
        foreign_keys=[work_company_cnpj]
    )

    groups: Mapped[Optional[list[Group]]] = relationship(
        "Group",
        secondary=user_group_many_to_many,
        backref='users',
        lazy='dynamic'
    )

    permissions: Mapped[Optional[list[Permission]]] = relationship(
        "Permission",
        secondary=user_permission_many_to_many,
        backref='users',
        lazy='dynamic'
    )


    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<User: {self.name}>"
