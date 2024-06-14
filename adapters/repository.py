from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract class to create repositories
    """

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs):
        """
        Criação do objeto.
        """

        raise ValueError("Implementação do método create é obrigatória")

    @classmethod
    @abstractmethod
    def retrieve(cls, *args, **kwargs):
        """
        Visualização dos dados de um objeto.
        """

        raise ValueError("Implementação do método retrieve é obrigatória")

    @classmethod
    @abstractmethod
    def list(cls, *args, **kwargs):
        """
        Listagem de objetos.
        """

        raise ValueError("Implementação do método list é obrigatória")

    @classmethod
    @abstractmethod
    def update(cls, *args, **kwargs):
        """
        Atualização de um objeto.
        """

        raise ValueError("Implementação do método update é obrigatória")

    @classmethod
    @abstractmethod
    def delete(cls, *args, **kwargs):
        """
        Deleção de um objeto.
        """

        raise ValueError("Implementação do método delete é obrigatória")
