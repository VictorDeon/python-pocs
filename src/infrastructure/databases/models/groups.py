from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.databases import BaseModel
from src.infrastructure.databases.models.__many_to_many import (
    group_permission_many_to_many
)
from .permissions import Permission


class Group(BaseModel):
    """
    Classe de grupos de usuários.
    """

    __tablename__ = "groups"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[Optional[datetime]] = Column(DateTime, nullable=True)
    is_deleted: Mapped[bool] = Column(Boolean, default=False, index=True)

    permissions: Mapped[Optional[list[Permission]]] = relationship(
        "Permission",
        secondary=group_permission_many_to_many,
        backref='groups',
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Group: {self.name}>"
