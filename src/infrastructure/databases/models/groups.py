from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
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
    __allow_unmapped__ = True

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    name: str = Column(String(50), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)

    permissions: Optional[list[Permission]] = relationship(
        "Permission",
        secondary=group_permission_many_to_many,
        backref='permission',
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Group: {self.name}>"
