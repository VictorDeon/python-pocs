from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from src.infrastructure.databases import BaseModel


class Permission(BaseModel):
    """
    Classe de permissões de usuários e/ou grupos.
    """

    __tablename__ = "permissions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(50), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)


    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Permission: {self.name}>"
