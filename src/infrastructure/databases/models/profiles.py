from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped
from src.infrastructure.databases import BaseModel


class Profile(BaseModel):
    """
    Classe de perfis de usuários.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    phone: Mapped[str] = Column(String(11), nullable=True)
    address: Mapped[str] = Column(String(100), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = Column(Boolean, default=False, index=True)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Profile: {self.id}>"
