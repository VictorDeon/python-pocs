from google.pubsub_v1 import SubscriberAsyncClient, PublisherAsyncClient, PubsubMessage, PublishRequest, AcknowledgeRequest
from google.api_core.retry_async import AsyncRetry
from google.api_core.exceptions import AlreadyExists
from typing import List, Any
import json


class PubsubSingleton:
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

        self.publisher = PublisherAsyncClient()
        self.subscriber = SubscriberAsyncClient()
        self.retry = AsyncRetry()

    @classmethod
    def get_instance(cls):
        """
        Pega a instância de cache.
        """

        if cls.__instance is None:
            cls.__instance = PubsubSingleton()

        return cls.__instance

    async def create_topic(self, project_id: str, topic_id: str) -> str:
        """
        Cria o tópico.
        """

        self.topic_path = self.publisher.topic_path(project_id, topic_id)
        try:
            await self.publisher.create_topic(name=self.topic_path, timeout=1, retry=self.retry)
        except AlreadyExists:
            pass

        return self.topic_path

    async def create_subscription(self, project_id: str, subscription_id: str) -> str:
        """
        Cria a subscription
        """

        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)
        try:
            await self.subscriber.create_subscription(
                name=self.subscription_path,
                topic=self.topic_path,
                ack_deadline_seconds=1,
                retry=self.retry
            )
        except AlreadyExists:
            await self.clean(self.subscription_path, 100)

        return self.subscription_path

    async def delete_topic(self, topic_path: str):
        """
        Deleta um topico.
        """

        await self.publisher.delete_topic(topic=topic_path, retry=self.retry)

    async def delete_subcription(self, subscription_path: str):
        """
        Deleta uma subscription.
        """

        await self.subscriber.delete_subscription(subscription=subscription_path, retry=self.retry)

    async def publish(self, topic_path: str, data: Any):
        """
        Publica algo na fila.
        """

        formated_data = json.dumps(data).encode('utf-8')
        message = PubsubMessage(data=formated_data)
        request = PublishRequest(topic=topic_path, messages=[message])
        await self.publisher.publish(request=request, retry=self.retry)

    async def pull(self, queue: str, max_messages: int):
        """
        Pega as mensagens da fila.
        """

        response = await self.subscriber.pull(
            subscription=queue,
            max_messages=max_messages,
            return_immediately=True,
            retry=self.retry
        )

        return response

    async def ack(self, queue: str, ack_id: str):
        """
        Realiza o ack da mensagem.
        """

        await self.subscriber.acknowledge(
            subscription=queue,
            ack_ids=[ack_id],
            retry=self.retry
        )

    async def unack(self, queue: str, ack_id: str):
        """
        Realiza o unack da mensagem
        """

        self.subscriber.modify_ack_deadline(
            subscription=queue,
            ack_ids=[ack_id],
            ack_deadline_seconds=0,
            retry=self.retry
        )

    async def clean(self, queue: str, max_messages: int):
        """
        Clean queue.
        """

        response = await self.pull(queue, max_messages)

        ack_list = []
        for received in response.received_messages:
            ack_list.append(received.ack_id)

        if ack_list:
            ack_request = AcknowledgeRequest(subscription=queue, ack_ids=ack_list)
            await self.subscriber.acknowledge(ack_request, retry=self.retry)

    async def get(self, queue: str, max_messages: int) -> List[dict]:
        """
        Pega os dado da sub enviados para um topico.
        """

        response = await self.pull(queue, max_messages)

        results = []
        for received in response.received_messages:
            data = json.loads(received.message.data.decode('utf-8'))
            if isinstance(data, list):
                results += data
            else:
                results.append(data)

        return results
