from sqlalchemy import select, Select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import ListCompaniesInputDTO
from ..models import Company


class ListCompanyDAO:
    """
    Repositorio de manipulação da entidade de empresa
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def list(self, dto: ListCompaniesInputDTO) -> list[Company]:
        """
        Pega uma lista de empresas e filtra elas.
        """

        statement: Select = select(Company)

        if dto:
            if dto.owner_id:
                statement: Select = statement.where(Company.owner_id == dto.owner_id)

            if dto.name:
                statement: Select = statement.where(Company.name.like(f"%{dto.name}%"))

        try:
            results = await self.session.scalars(statement=statement)
            companies: list[Company] = results.all()
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao listar as empresas: {e}")
            raise e

        return companies

    async def count(self) -> int:
        """
        Pega a quantidade de empresas registradas no banco.
        """

        statement: Select = select(func.count(Company.cnpj))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao realizar a contagem de empresas: {e}")
            raise e

        return qtd
