from typing import Optional
from sqlalchemy import VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.databases import BaseModel


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
