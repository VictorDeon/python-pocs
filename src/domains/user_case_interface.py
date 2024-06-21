from typing import Any
from abc import ABC, abstractmethod


class UserCaseInterface(ABC):
    """
    Interface de casos de uso.
    """

    @abstractmethod
    async def execute(self, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """
