from typing import TypeVar, Generic
from abc import ABCMeta, abstractmethod

IN = TypeVar("IN")
OUT = TypeVar("OUT")


class UserCaseInterface(Generic[IN, OUT], metaclass=ABCMeta):
    """
    Interface de casos de uso.
    """

    @abstractmethod
    async def execute(self, input_dto: IN) -> OUT:
        """
        Executa o caso de uso.
        """
