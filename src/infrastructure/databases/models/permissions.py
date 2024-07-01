from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.databases import BaseModel


class Permission(BaseModel):
    """
    Classe de permissões de usuários e/ou grupos.
    """

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    code: Mapped[str] = mapped_column(VARCHAR(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Permission: {self.name}>"
