from typing import Any


class Mediator:
    """
     Implementação particular do Mediador, que coordena a
     interação entre os diferentes recebedores a partir de um comando.
    """

    def __init__(self):
        """
        Cria uma lista de recebedores que irão receber as mensagens.
        """

        self.receivers: list[Any] = []

    def add(self, receiver: Any):
        """
        Adiciona os colegas na lista de contatos.
        """

        self.receivers.append(receiver)

    async def send(self, command: str, *args, **kwargs) -> Any:
        """
        Envia a mensagem a alguma plataforma.
        """

        for receiver in self.receivers:
            if receiver.command == command:
                if command == "BlockingRequestSync":
                    return receiver.execute(*args, **kwargs)
                else:
                    return await receiver.execute(*args, **kwargs)
