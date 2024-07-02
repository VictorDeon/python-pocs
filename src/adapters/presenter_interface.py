from abc import ABCMeta, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Generic

MODEL = TypeVar("MODEL")
OUTPUT = TypeVar("OUTPUT")


class PresenterInterface(Generic[MODEL, OUTPUT], metaclass=ABCMeta):
    """
    Interface de saída das APIs.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session

    @abstractmethod
    def present(self, model: MODEL) -> OUTPUT:
        """
        Forma final de apresentação dos dados.
        """
