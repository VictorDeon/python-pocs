from asyncio import Queue, Event
import time
import random
import asyncio
import logging
import signal


logging.basicConfig(level=logging.INFO)

# Quantidade de trabalhadores rodando, podemos colocar como a quantidade
# de itens do pubsub que pegaremos por vez para processar.
MAX_PARALLEL_TASKS = 10


async def get_external_messages(messages) -> list[int]:
    """
    Método para gerar mensagens aleatórias.
    Pode ser um método que pega as mensagens de um pubsub. 
    """

    logging.info(f"Gerando {messages} números randomicos.")
    return [random.randint(0, 15) for _ in range(messages)]


async def task_processor(message: int) -> None:
    """
    Método que processa a mensagem, colocamos um sleep para
    simular o processamento.
    """

    logging.info(f'Processando mensagem: {message}')
    await asyncio.sleep(message)
    if not random.randint(0, 10):
        raise Exception(f"Mensagem {message} deu um error interno.")

    logging.info(f'Processamento da mensagem {message} finalizada com sucesso.')


async def task_subscriber(queue: Queue, stop_event: Event) -> None:
    """
    Tarefa que observa preenche a fila interna do python com mais mensagens
    que vierem externamente.    
    """

    total_messages = 0
    start = time.time()
    while True:
        if stop_event.is_set():
            return

        messages_to_get = MAX_PARALLEL_TASKS - queue.qsize()
        if messages_to_get <= 0:
            await asyncio.sleep(1)
            continue

        total_messages += messages_to_get
        print(f"{time.time() - start} - Total de mensagens: {total_messages}")

        try:
            # Como se fosse o pubsub
            messages = await asyncio.wait_for(get_external_messages(messages_to_get), timeout=10)
        except asyncio.TimeoutError:
            logging.error("Disparou um timeout quando ao receber as mensagens externas.")
            await asyncio.sleep(1)
            stop_event.set()
            continue
        except Exception:
            logging.exception("Ocorreu um error interno.")
            await asyncio.sleep(5)
            continue

        if not messages:
            await asyncio.sleep(1)
            continue

        for message in messages:
            await queue.put(message)


async def task_worker(queue: Queue, stop_event: Event) -> None:
    """
    Processa as mensagens que chega na fila interna.
    """

    while True:
        if stop_event.is_set():
            return

        try:
            value = queue.get_nowait()
        except asyncio.QueueEmpty:
            await asyncio.sleep(0.5)
            continue

        try:
            await asyncio.wait_for(task_processor(value), timeout=300)
        except Exception:
            logging.exception(f"Ocorreu um error ao processar a mensagem: {value}")
            await asyncio.sleep(1)
            # colocar mensagem na fila novamente, no caso do pubsub, acho que é melhor deixar dar
            # erro e ir pra dlq
            # await queue.put(value)
            continue


def setup_signal_handler(stop_event: Event) -> None:
    """
    Configura o gracefull shutdown caso algum sinal externo acabe
    desligando o código no momento em que as mensagens estão processando.    
    """

    loop = asyncio.get_event_loop()

    def shutdown(sig):
        if stop_event.is_set():
            logging.info(f"Foi recebido o sinal {sig.name}, já estamos parando o script.")
            return

        logging.info(f"Foi recebido o sinal {sig.name}, parando o script.")
        stop_event.set()

    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown, sig)


async def main() -> None:
    """
    Método principal de execução.    
    """

    stop_event: Event = Event()
    setup_signal_handler(stop_event)

    queue: Queue = Queue()
    tasks = []

    subscriber_task = asyncio.create_task(task_subscriber(queue, stop_event))
    tasks.append(subscriber_task)
    for i in range(MAX_PARALLEL_TASKS):
        worker_task = asyncio.create_task(task_worker(queue, stop_event))
        tasks.append(worker_task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
