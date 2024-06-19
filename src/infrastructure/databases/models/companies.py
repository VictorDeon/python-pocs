from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from src.infrastructure.databases import BaseModel


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    cnpj: str = Column(String(14), nullable=False, index=True)
    name: str = Column(String(50), nullable=False)
    fantasy_name: str = Column(String(50), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_deleted: bool = Column(Boolean, default=False, index=True)

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
