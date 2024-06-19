from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.databases import BaseModel
from .users import User


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"
    __allow_unmapped__ = True

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    cnpj: str = Column(String(14), nullable=False, index=True)
    name: str = Column(String(50), nullable=False)
    fantasy_name: str = Column(String(50), nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.now, index=True)
    updated_at: datetime = Column(DateTime, nullable=True)
    is_actived: bool = Column(Boolean, default=True, index=True)

    id_user: int = Column(BigInteger, ForeignKey("users.id"))
    user: User = relationship("User", lazy="joined", backref='companies')

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
