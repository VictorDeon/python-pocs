import asyncio
import signal
import random

stop_event = asyncio.Event()


def shutdown(sig: signal.Signals) -> None:
    """
    Setando o evento de parada.    
    """

    print(f"Sinal de sair recebido: {sig.name}")
    stop_event.set()
    print("Evento de parada setado.")


def setup_signal_handler() -> None:
    """
    Observador de sinais como o Ctrl + C para parada
    do script ou graceful shutdown.    
    """

    loop = asyncio.get_running_loop()

    # kill -l (mostra todos os comandos de sinais)
    # SIGKILL -> Mata o processo forçado e não tem oq fazer (kill -9)
    # SIGHUP -> Recebeu um evento de desligamento do processo (desescalonamento de um pod)
    # SIGTERM -> Recebeu um evento para terminar o processo (parada de um pod)
    # SIGINT -> Recebeu um evento de interrupção (Ctrl+C)
    # Se ocorrer qualquer um desses sinais execute o evento de parada (shutdown)
    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown, sig)


async def worker(n, stop_event) -> None:
    """
    Trabalhador processando algo de forma simulada com o
    sleep de 1 a 15 de forma randomica.    
    """

    while True:
        print(f"Worker {n}")
        if stop_event.is_set():
            print(f"Worker {n}: Evento de parada setado. Parando.")
            break

        await asyncio.sleep(random.randint(1, 15))


async def main() -> None:
    """
    Tetando o graceful shutdown.
    """

    setup_signal_handler()

    # Criando 6 tarefas
    tasks = []
    for n in range(6):
        task = worker(n, stop_event)
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
    print("Loop de eventos parou.")
