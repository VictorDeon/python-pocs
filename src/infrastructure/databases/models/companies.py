from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.databases import BaseModel
from .users import User


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"

    cnpj: Mapped[str] = Column(String(14), primary_key=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    fantasy_name: Mapped[str] = Column(String(50), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=True)
    is_actived: Mapped[bool] = Column(Boolean, default=True, index=True)

    owner_id: Mapped[int] = Column(BigInteger, ForeignKey("users.id", name='fk_company_owner'))
    owner: Mapped[User] = relationship(
        "User",
        back_populates='companies',
        foreign_keys=[owner_id]
    )

    employees: Mapped[Optional[list[User]]] = relationship(
        'User',
        back_populates='work_company',
        foreign_keys='User.work_company_cnpj'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
