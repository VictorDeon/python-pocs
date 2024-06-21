from src.adapters.dtos import ListPokemonsInputDTO, ListPokemonsOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Pokemon
from src.infrastructure.requests import RequestRepositoryInterface


class ListPokemonsUseCase:
    """
    Realiza o caso de uso de listar os pokemons.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Pokemon, ListPokemonsOutputDTO],
        repository: RequestRepositoryInterface[Pokemon]):
        """
        Construtor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: ListPokemonsInputDTO):
        """
        Executa o caso de uso.
        """

        pokemons = await self.repository.list(
            limit=input_dto.limit,
            offset=input_dto.offset
        )
        return self.presenter.present(pokemons)
