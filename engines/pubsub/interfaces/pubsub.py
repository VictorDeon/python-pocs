from abc import ABC, abstractmethod
from typing import List, Any


class PubsubSingletonInterface(ABC):
    """
    Singleton para mapeamento de filas do pubsub
    """

    __instance = None

    def __init__(self):
        """
        Construtor do cliente.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do pubsub já existe! Utilize a função get_instance()")

    @classmethod
    def get_instance(cls):
        """
        Pega a instância de cache.
        """

        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    @abstractmethod
    async def create_pubsub(self) -> None:
        """
        Cria as instâncias do pubsub a partir do cloud escolhido.
        """

        pass

    @abstractmethod
    async def create_topic(self, project_id: str, topic_id: str) -> str:
        """
        Cria o tópico.
        """

        pass

    @abstractmethod
    async def create_subscription(self, project_id: str, subscription_id: str) -> str:
        """
        Cria a subscription
        """

        pass

    @abstractmethod
    async def delete_topic(self, topic_path: str):
        """
        Deleta um topico.
        """

        pass

    @abstractmethod
    async def delete_subcription(self, subscription_path: str):
        """
        Deleta uma subscription.
        """

        pass

    @abstractmethod
    async def publish(self, topic_path: str, data: Any):
        """
        Publica algo na fila.
        """

        pass

    @abstractmethod
    async def pull(self, queue: str, max_messages: int):
        """
        Pega as mensagens da fila.
        """

        pass

    @abstractmethod
    async def ack(self, queue: str, ack_id: str):
        """
        Realiza o ack da mensagem.
        """

        pass

    @abstractmethod
    async def unack(self, queue: str, ack_id: str):
        """
        Realiza o unack da mensagem
        """

        pass

    @abstractmethod
    async def clean(self, queue: str, max_messages: int):
        """
        Clean queue.
        """

        pass

    @abstractmethod
    async def get(self, queue: str, max_messages: int) -> List[dict]:
        """
        Pega os dado da sub enviados para um topico.
        """

        pass
