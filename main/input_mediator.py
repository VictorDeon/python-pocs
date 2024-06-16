from typing import Any


class InputAdapterMediator:
    """
    Classe mediadora de comunicação.
    """

    def __init__(self):
        """
        Cria a lista de adaptadores que irão receber a mensagem.
        """

        self.controllers: list = []

    def add(self, controller) -> None:
        """
        Adicionar as controladoras a lista de controllers.
        """

        self.controllers.append(controller)

    def send(self, sender: Any, *args, **kwargs):
        """
        Envia a mensagem a um recebedor.
        """

        for controller in self.controllers:
            if controller != sender:
                controller.receive(*args, **kwargs)
