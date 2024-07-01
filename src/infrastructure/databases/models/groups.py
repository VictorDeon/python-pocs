from sqlalchemy import VARCHAR, BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.databases import BaseModel


class Group(BaseModel):
    """
    Classe de grupos de usuários.
    """

    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Group: {self.name}>"
