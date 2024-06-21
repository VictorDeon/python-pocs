from typing import TypeVar, Generic, Any
from abc import ABCMeta, abstractmethod

T = TypeVar("T")


class UserCaseInterface(Generic[T], metaclass=ABCMeta):
    """
    Interface de casos de uso.
    """

    @abstractmethod
    async def execute(self, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """
