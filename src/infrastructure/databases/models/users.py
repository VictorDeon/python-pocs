from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..base import Base


class User(Base):
    """
    Classe de usuários.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String(20), nullable=False)
    pet_id = relationship("Pet")

    def __repr__(self) -> str:
        """
        Objeto como string.
        """

        return f"User {self.name}"
