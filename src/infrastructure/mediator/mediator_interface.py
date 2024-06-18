from abc import ABC, abstractmethod
from typing import Any


class MediatorInterface(ABC):
    """
    Interface que padroniza as operações que serão chamadas.
    """

    @abstractmethod
    async def send(self, receiver: Any, *args, **kwargs) -> Any:
        """
        Envia a mensagem para algum recebedor especifico.
        """

        pass
