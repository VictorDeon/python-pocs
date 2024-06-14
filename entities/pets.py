from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from engines.db import Base
import enum


class SpecieSet(enum.Enum):
    """
    Tipos de especies de pet.
    """

    DOG = "dog"
    CAT = "cat"
    FISH = "fish"
    TURTLE = "turtle"


class Pet(Base):
    """
    Classe de pets.
    """

    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    specie = Column(Enum(SpecieSet), nullable=False)
    age = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __rep__(self):
        """
        Objeto como string.
        """

        return f"Pet {self.name}"
