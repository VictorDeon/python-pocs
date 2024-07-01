from typing import Optional
from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.databases import BaseModel


class Profile(BaseModel):
    """
    Classe de perfis de usuários.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(11), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=True)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Profile: {self.id}>"
