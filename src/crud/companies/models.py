from typing import Optional
from sqlalchemy import VARCHAR, BIGINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.engines.databases import BaseModel


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"

    cnpj: Mapped[str] = mapped_column(VARCHAR(14), primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    fantasy_name: Mapped[Optional[str]] = mapped_column(VARCHAR(50), nullable=True)

    owner_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey(
            "users.id",
            name='fk_company_owner',
            ondelete="CASCADE"
        )
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
