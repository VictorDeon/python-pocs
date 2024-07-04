from timeit import repeat
from cProfile import Profile
from pstats import Stats
from statistics import mean
from memory_profiler import profile
from src.adapters import ControllerInterface
from src.adapters.dtos import ProfileRequestsOutputDTO


class ProfileRequestController(ControllerInterface):
    """
    Realiza uma requisição quantas vezes for necessário de uma função
    e retorna o resultado.
    """

    @profile()
    def memory_consume(self):
        """
        Abrindo arquivo
        """

        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        del b
        return a

    async def execute(self, qtd: int, sort: str) -> ProfileRequestsOutputDTO:
        """
        Essa requisição executa códigos
        """

        profile = Profile()
        profile.enable()

        result = repeat(self.memory_consume, repeat=1, number=qtd)
        result_min = min(result)
        result_max = max(result)
        result_mean = mean(result)
        result_total = sum(result)

        result = ProfileRequestsOutputDTO(
            min=round(result_min, 4),
            max=round(result_max, 4),
            mean=round(result_mean, 4),
            total=round(result_total, 4)
        )

        profile.disable()
        stats = Stats(profile).sort_stats(sort)
        stats.print_stats()

        return result
