from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from src.infrastructure.databases import BaseModel
from .users import User


class Company(BaseModel):
    """
    Classe de empresas.
    """

    __tablename__ = "companies"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = Column(String(14), nullable=False, index=True)
    name: Mapped[str] = Column(String(50), nullable=False)
    fantasy_name: Mapped[str] = Column(String(50), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, index=True)
    updated_at: Mapped[datetime] = Column(DateTime, nullable=True)
    is_actived: Mapped[bool] = Column(Boolean, default=True, index=True)

    id_user: Mapped[int] = Column(BigInteger, ForeignKey("users.id"))
    user: Mapped[User] = relationship("User", lazy="joined", backref='companies')

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"<Company: {self.name}>"
