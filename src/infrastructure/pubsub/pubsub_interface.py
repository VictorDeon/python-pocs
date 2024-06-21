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

        self.publisher = None
        self.subscriber = None
        self.retry = None
        self.topic_path = None
        self.subscription_path = None

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

    @abstractmethod
    async def create_topic(self, project_id: str, topic_id: str) -> str:
        """
        Cria o tópico.
        """

    @abstractmethod
    async def create_subscription(self, project_id: str, subscription_id: str) -> str:
        """
        Cria a subscription
        """

    @abstractmethod
    async def delete_topic(self, topic_path: str):
        """
        Deleta um topico.
        """

    @abstractmethod
    async def delete_subcription(self, subscription_path: str):
        """
        Deleta uma subscription.
        """

    @abstractmethod
    async def publish(self, topic_path: str, data: Any):
        """
        Publica algo na fila.
        """

    @abstractmethod
    async def pull(self, queue: str, max_messages: int):
        """
        Pega as mensagens da fila.
        """

    @abstractmethod
    async def ack(self, queue: str, ack_id: str):
        """
        Realiza o ack da mensagem.
        """

    @abstractmethod
    async def unack(self, queue: str, ack_id: str):
        """
        Realiza o unack da mensagem
        """

    @abstractmethod
    async def clean(self, queue: str, max_messages: int):
        """
        Clean queue.
        """

    @abstractmethod
    async def get(self, queue: str, max_messages: int) -> List[dict]:
        """
        Pega os dado da sub enviados para um topico.
        """
