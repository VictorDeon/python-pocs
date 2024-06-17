from abc import ABC, abstractmethod
from src.adapters.interfaces import PresenterInterface
from typing import Any


class UserCaseInterface(ABC):
    """
    Interface de casos de uso.
    """

    @abstractmethod
    def execute(self, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """

        pass
