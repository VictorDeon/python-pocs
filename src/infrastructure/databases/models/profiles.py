from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from src.infrastructure.databases import BaseModel


class Profile(BaseModel):
    """
    Classe de perfis de usuários.
    """

    __tablename__ = "profiles"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    phone: str = Column(String(11), nullable=True)
    address: str = Column(String(100), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)


    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Profile: {self.id}>"
