import logging
from typing import Optional
from sqlalchemy import (
    select, Select, func,
    insert, Insert,
    update as sql_update, Update,
    delete as sql_delete, Delete
)
from src.adapters.dtos import (
    CreateCompanyInputDTO, ListCompaniesInputDTO,
    UpdateCompanyInputDTO
)
from src.infrastructure.databases.models import Company
from src.infrastructure.databases import DAOInterface


class CompanyDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de empresa
    """

    async def create(self, dto: CreateCompanyInputDTO, commit: bool = True) -> Company:
        """
        Cria a empresa passando como argumento os dados da mesma.
        """

        try:
            statement: Insert = insert(Company).values(**dto.to_dict()).returning(Company)
            company: Company = await self.session.scalar(statement)

            if commit:
                await self.session.commit()
                logging.info("Empresa inseridada no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao criar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company

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
            logging.error(f"Ocorreu um problema ao listar as empresas: {e}")
            raise e

        return companies

    async def get_by_cnpj(self, cnpj: str) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo cnpj
        """

        statement: Select = select(Company).where(Company.cnpj == cnpj)
        try:
            company: Company = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao pegar os dados da empresa: {e}")
            raise e

        return company

    async def update(self, cnpj: str, dto: UpdateCompanyInputDTO, commit: bool = True) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo _id e atualiza
        """

        statement: Update = sql_update(Company).values(**dto.to_dict()).where(Company.cnpj == cnpj).returning(Company)

        try:
            company: Company = await self.session.scalar(statement)

            if commit:
                await self.session.commit()
                logging.info("Empresa atualizada no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao atualizar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company

    async def delete(self, cnpj: str, commit: bool = True) -> str:
        """
        Pega os dados de uma empresa pelo _id e deleta ela
        """

        statement: Delete = sql_delete(Company).where(Company.cnpj == cnpj).returning(Company.id)

        try:
            company_cnpj: str = await self.session.scalar(statement)
            if not company_cnpj:
                raise ValueError(f"Empresa com o cnpj {company_cnpj} não encontrado.")

            if commit:
                await self.session.commit()
                logging.info("Empresa deletada do banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao deletar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company_cnpj

    async def count(self) -> int:
        """
        Pega a quantidade de empresas registradas no banco.
        """

        statement: Select = select(func.count(Company.cnpj))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao realizar a contagem de empresas: {e}")
            raise e

        return qtd
