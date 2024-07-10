import asyncio
from datetime import datetime
from asyncio import Queue


async def generate_data(qtd: int, queue: Queue) -> None:
    """
    Gera os dados
    """

    print(f"Aguarde a geração de {qtd} dados")

    for index in range(1, qtd + 1):
        n = index * index
        await queue.put((n, datetime.now()))
        await asyncio.sleep(0.001)

    print(f"{qtd} dados gerados com sucesso.")


async def process_data(qtd: int, queue: Queue) -> None:
    """
    Processa os dados.
    """

    print(f"Aguarde o processament de {qtd} dados.")
    processed = 0
    while processed < qtd:
        await queue.get()
        processed += 1
        await asyncio.sleep(0.001)

    print(f"Foram processados {qtd} dados.")


if __name__ == "__main__":
    total = 5_000
    queue = Queue()
    event_loop = asyncio.get_event_loop()

    print(f"Computando {total * 2:.2f} dados")
    event_loop.run_until_complete(generate_data(qtd=total, queue=queue))
    event_loop.run_until_complete(generate_data(qtd=total, queue=queue))
    event_loop.run_until_complete(process_data(qtd=total * 2, queue=queue))
    event_loop.close()
