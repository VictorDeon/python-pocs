from multiprocessing import Process, Pipe, current_process, Event as MultiprocessingEvent
from multiprocessing.synchronize import Event
from multiprocessing.connection import Connection
import time


def ping(pipe: Connection, stop_event: Event) -> None:
    """
    Envia e recebe mensagem
    """

    process_name = current_process().name

    while not stop_event.is_set():
        message: str = pipe.recv()
        if message.lower() == 'sair':
            pipe.send('sair')
            break

        pipe.send(message)
        print(f"Processo {process_name} enviou:", message)


def pong(pipe: Connection, stop_event: Event) -> None:
    """
    Envia e recebe mensagem.
    """

    process_name = current_process().name

    while not stop_event.is_set():
        message: str = pipe.recv()
        if message.lower() == 'sair':
            pipe.send('sair')
            break

        pipe.send(message)
        print(f"Processo {process_name} enviou:", message)


def main() -> None:
    """
    Função de execução.
    """

    parent_ping, child_ping = Pipe()
    parent_pong, child_pong = Pipe()
    stop_event = MultiprocessingEvent()

    process_ping = Process(name="ping", target=ping, args=(child_ping, stop_event))
    process_pong = Process(name="pong", target=pong, args=(child_pong, stop_event))

    process_ping.start()
    process_pong.start()

    while not stop_event.is_set():
        time.sleep(2)
        ping_input = input(f"Digite uma mensagem para enviar ao {process_ping.name} (ou 'sair' para terminar): ")
        if ping_input.lower() == 'sair':
            parent_ping.send('sair')
            parent_pong.send('sair')
            stop_event.set()
        else:
            parent_ping.send(ping_input)

        time.sleep(2)
        pong_input = input(f"Digite uma mensagem para enviar ao {process_pong.name} (ou 'sair' para terminar): ")
        if pong_input.lower() == 'sair':
            parent_ping.send('sair')
            parent_pong.send('sair')
            stop_event.set()
        else:
            parent_pong.send(pong_input)

    process_ping.join()
    process_pong.join()

    print("Ping Pong concluido.")


if __name__ == '__main__':
    main()
