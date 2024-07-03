from timeit import repeat
from statistics import mean
from src.adapters import ControllerInterface
from src.adapters.dtos import ProfileRequestsOutputDTO


class ProfileRequestTimeitController(ControllerInterface):
    """
    Realiza uma requisição quantas vezes for necessário de uma função
    e retorna o resultado.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "TimeIt"

    async def execute(self, func: str, qtd: int) -> ProfileRequestsOutputDTO:
        """
        Essa requisição executa códigos
        """

        result = repeat(func, number=qtd)
        result_min = min(result)
        result_max = max(result)
        result_mean = mean(result)
        result_total = sum(result)

        return ProfileRequestsOutputDTO(
            min=round(result_min, 4),
            max=round(result_max, 4),
            mean=round(result_mean, 4),
            total=round(result_total, 4)
        )
