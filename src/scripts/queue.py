import time
import random
import asyncio
import signal
import os
from asyncio import Queue, Event
import asyncer
from google.api_core.exceptions import GoogleAPIError
from src.engines.logger import ProjectLoggerSingleton
from src.engines.pubsub import GCPPubsubSingleton


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
TOPIC_ID = os.environ.get("TOPIC_ID")
SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID")
MAX_MESSAGES = os.environ.get("MAX_MESSAGES", 1)
EVALUATE_MESSAGE_TIMEOUT = os.environ.get("EVALUATE_MESSAGE_TIMEOUT", 600)
QUEUE = f"projects/{PROJECT_ID}/subscriptions/{SUBSCRIPTION_ID}"
logger = ProjectLoggerSingleton.get_logger()


def force_shutdown():
    """
    Força o shutdown do serviço.
    """

    os.kill(os.getpid(), signal.SIGINT)


def write_health_check():
    """
    Escrevendo o arquivo de health check.
    """

    with open(".timestamp.healthcheck", "w", encoding='utf-8') as file:
        file.write(str(time.time()))


async def get_messages_from_pubsub_and_put_in_queue(message_queue: Queue, pubsub: GCPPubsubSingleton):
    """
    Pega as mensagens do pubsub da google e envia para a fila do python.
    """

    messages_to_get = MAX_MESSAGES - message_queue.qsize()
    logger.debug(f"Pegando {messages_to_get} mensagens do pubsub")

    if messages_to_get <= 0:
        logger.debug("Fila lotada...")
        return

    try:
        logger.debug("Pegando mensagens do pubsub.")
        response = await asyncio.wait_for(pubsub.pull(QUEUE, messages_to_get), timeout=10)
    except asyncio.TimeoutError:
        logger.error("A fila deu timeout. Desligando o serviço.")
        await asyncer.asyncify(force_shutdown)
        return
    except GoogleAPIError as error:
        logger.error(f"Fila bloqueada: {str(error)}. Desligando o serviço.")
        await asyncer.asyncify(force_shutdown)
        return
    except Exception as error:
        logger.exception(f"Fila morreu: {str(error)}. Desligando o serviço.")
        await asyncer.asyncify(force_shutdown)
        return

    if len(response.received_messages) == 0:
        return

    logger.debug(f"Foi recebido {len(response.received_messages)} mensagens para inserção na fila local.")
    for message in response.received_messages:
        logger.debug(f"Inserindo a mensagem {message.ack_id} na fila local")
        await message_queue.put(message)


async def subscribe_worker(message_queue: Queue, stop_event: Event):
    """
    Inicia o consumidor da fila de avaliação.
    """

    pubsub = GCPPubsubSingleton.get_instance()

    while True:
        logger.debug("SUBSCRIBER WORKER: Checando o evento de parada.")
        if stop_event.is_set():
            logger.warning("SUBSCRIBER WORKER: Evento de parada ativado. Desligando serviço.")
            break

        logger.debug("SUBSCRIBER WORKER: Escrevendo arquivo health check")
        await asyncer.asyncify(write_health_check)

        logger.debug("SUBSCRIBER WORKER: Pegando as mensagens do pubsub e inserindo na fila local")
        await get_messages_from_pubsub_and_put_in_queue(message_queue, pubsub)
        await asyncio.sleep(1)


async def process_message(message, pubsub: GCPPubsubSingleton):
    """
    Processa a mensagem
    """

    try:
        # Simular o processamento da mensagem com 90% de sucesso.
        success = True
        random_number = random.randint(0, 10)
        await asyncio.sleep(random_number)
        if not random_number:
            success = False

        if success:
            logger.info(f"Mensagem {message.ack_id} processada com sucesso.")
            await asyncio.wait_for(pubsub.ack(QUEUE, message.ack_id), timeout=10)
        else:
            logger.error(f"Mensagem {message.ack_id} processada com erros.")
            await asyncio.wait_for(pubsub.unack(QUEUE, message.ack_id), timeout=10)
    except Exception as error:
        logger.error(f'Error na mensagem: {str(message.ack_id)} error {str(error)}')
        await asyncio.wait_for(pubsub.unack(QUEUE, message.ack_id), timeout=10)


async def process_message_worker(queue: Queue, stop_event: Event):
    """
    Dispara o worker que vai processar as mensagens
    """

    pubsub = GCPPubsubSingleton.get_instance()

    while True:
        logger.debug("PROCESS MESSAGE WORKER: Checando o evento de parada.")
        if stop_event.is_set():
            logger.warning("PROCESS MESSAGE WORKER: Evento de parada ativado. Desligando serviço.")
            break

        try:
            logger.debug("PROCESS MESSAGE WORKER: Pegando mensagens da fila local.")
            message = queue.get_nowait()
            try:
                logger.debug(f"Processando messagem {message.ack_id}")
                await asyncio.wait_for(process_message(message, pubsub), timeout=EVALUATE_MESSAGE_TIMEOUT)
                logger.debug(f"Mensagem {message.ack_id} processada com sucesso.")
            except asyncio.TimeoutError:
                logger.error(f'Timeout no processamento da mensagem {message.ack_id}.')
                await asyncio.wait_for(pubsub.unack(queue, message.ack_id), timeout=10)
            except Exception as error:
                logger.error(f'Error no processamento da mensagem {message.ack_id}: {error}')
                await asyncio.wait_for(pubsub.unack(queue, message.ack_id), timeout=10)
        except asyncio.QueueEmpty:
            logger.debug("PROCESS MESSAGE WORKER: Queue empty.")
        except Exception as error:
            logger.error(f'Error ao processar mensagem: {str(error)}. Desligando o serviço.')
            await asyncer.asyncify(force_shutdown)
            return

        await asyncio.sleep(0.5)


async def main() -> None:
    """
    Método principal de execução.
    """

    stop_event: Event = Event()
    pubsub = GCPPubsubSingleton.get_instance()
    message_queue = Queue(maxsize=MAX_MESSAGES + 1)
    all_tasks = []

    if os.environ.get("PUBSUB_EMULATOR_HOST"):
        await pubsub.create_topic(PROJECT_ID, TOPIC_ID)
        await pubsub.create_subscription(PROJECT_ID, SUBSCRIPTION_ID)

    all_tasks.append(
        asyncio.create_task(subscribe_worker(message_queue, stop_event))
    )

    for _ in range(MAX_MESSAGES):
        all_tasks.append(
            asyncio.create_task(process_message_worker(message_queue, stop_event))
        )

    await asyncio.gather(*all_tasks)

if __name__ == '__main__':
    asyncio.run(main())
