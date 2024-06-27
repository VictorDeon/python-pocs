from datetime import datetime
from typing import Optional
from sqlalchemy import String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.databases import BaseModel


class Profile(BaseModel):
    """
    Classe de perfis de usuários.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    phone: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    user: Mapped["User"] = relationship(
        "User",
        single_parent=True,
        back_populates="profile"
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Profile: {self.id}>"
