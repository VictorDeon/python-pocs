import multiprocessing


def ping(connection):
    """
    Envia e recebe mensagem.
    """

    msg = input("PING escreva a msg: ")
    connection.send(msg)
    received_msg = connection.recv()
    print(f"PING recebeu a msg: {received_msg}")


def pong(connection):
    """
    Envia e recebe mensagem.
    """

    received_msg = connection.recv()
    print(f"PONG recebeu a msg: {received_msg}")
    msg = input("PONG escreva a msg: ")
    connection.send(msg)


def main():
    """
    Função de execução.
    """

    connection_ping, connection_pong = multiprocessing.Pipe(duplex=True)

    process_ping = multiprocessing.Process(target=ping, args=(connection_ping,))
    process_pong = multiprocessing.Process(target=pong, args=(connection_pong,))

    while True:
        process_ping.start()
        process_pong.start()
        process_ping.join()
        process_pong.join()


if __name__ == '__main__':
    main()
