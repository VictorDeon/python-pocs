from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"

    cnpj: Mapped[str] = mapped_column(String(14), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    fantasy_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_actived: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", name='fk_company_owner'))
    owner: Mapped["User"] = relationship(
        "User",
        back_populates='companies',
        foreign_keys=[owner_id]
    )

    employees: Mapped[Optional[list["User"]]] = relationship(
        'User',
        back_populates='work_company',
        foreign_keys='User.work_company_cnpj'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
