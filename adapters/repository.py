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

        pass

    @classmethod
    @abstractmethod
    def retrieve(cls, *args, **kwargs):
        """
        Visualização dos dados de um objeto.
        """

        pass

    @classmethod
    @abstractmethod
    def list(cls, *args, **kwargs):
        """
        Listagem de objetos.
        """

        pass

    @classmethod
    @abstractmethod
    def update(cls, *args, **kwargs):
        """
        Atualização de um objeto.
        """

        pass

    @classmethod
    @abstractmethod
    def delete(cls, *args, **kwargs):
        """
        Deleção de um objeto.
        """

        pass
