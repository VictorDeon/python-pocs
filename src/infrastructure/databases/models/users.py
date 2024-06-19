from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from src.infrastructure.databases import BaseModel


class User(BaseModel):
    """
    Classe de usuários.
    """

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(50), nullable=False, index=True, unique=True)
    password: str = Column(String(30), nullable=False)
    name: str = Column(String(30), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<User: {self.name}>"
