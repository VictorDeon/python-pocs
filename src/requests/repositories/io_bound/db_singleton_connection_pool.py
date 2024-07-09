from time import time
from faker import Faker
from src.engines.logger import ProjectLoggerSingleton
from src.engines.databases import DBConnectionSingleton
from src.crud.permissions.repositories import CreatePermissionDAO, DeletePermissionDAO
from src.crud.permissions.dtos import CreatePermissionInputDTO
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocDBSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do db singleton.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "DBSingletonConnectionPool"
        self.faker = Faker()

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        db = await DBConnectionSingleton.get_instance()

        repository = CreatePermissionDAO(session=db.session)
        model = await repository.execute(dto=CreatePermissionInputDTO(
            name=self.faker.name(),
            code=self.faker.email()
        ))

        repository = DeletePermissionDAO(session=db.session)
        await repository.execute(_id=model.id)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
