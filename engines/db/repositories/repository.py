from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract class to create repositories
    """

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Criação do objeto.
        """

        raise ValueError("Implementação do método create é obrigatória")

    @abstractmethod
    def retrieve(self, *args, **kwargs):
        """
        Visualização dos dados de um objeto.
        """

        raise ValueError("Implementação do método retrieve é obrigatória")

    @abstractmethod
    def list(self, *args, **kwargs):
        """
        Listagem de objetos.
        """

        raise ValueError("Implementação do método list é obrigatória")

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Atualização de um objeto.
        """

        raise ValueError("Implementação do método update é obrigatória")

    @abstractmethod
    def delete(self, *args, **kwargs):
        """
        Deleção de um objeto.
        """

        raise ValueError("Implementação do método delete é obrigatória")
