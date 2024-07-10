import time
from typing import Generator
from ...dtos import PocRequestsOutputDTO
from src.engines.logger import ProjectLoggerSingleton

logger = ProjectLoggerSingleton.get_logger()


def fibonacci() -> Generator[int, None, None]:
    """
    Fibonacci usando geradores
    """

    value: int = 0
    next_value: int = 1

    while True:
        value, next_value = next_value, value + next_value
        yield value


class GeneratorRepository:
    """
    Aqui termos um exemplo de fibonacci usando geradores ou mais conhecidos como corotines.
    É a base para o uso de corotines em python
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "GeneratorRequest"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Essa requisição executa fibonnati usando geradores.
        """

        start_time = time.time()
        logger.info(f"Iniciando a chamada {self.command}")

        result = []
        for n in fibonacci():
            if n > 100:
                break

            result.append(str(n))

        logger.info(f"Resultado: {', '.join(result)}")
        end_time = time.time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
