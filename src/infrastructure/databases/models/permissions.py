from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped
from src.infrastructure.databases import BaseModel


class Permission(BaseModel):
    """
    Classe de permissões de usuários e/ou grupos.
    """

    __tablename__ = "permissions"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    code: Mapped[str] = Column(String(20), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = Column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = Column(Boolean, default=False, index=True)


    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Permission: {self.name}>"
