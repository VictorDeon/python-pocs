import logging
from typing import Optional
from sqlalchemy import select, Select
from sqlalchemy.orm.exc import NoResultFound
from src.adapters.dtos import (
    CreateCompanyInputDTO, ListCompaniesInputDTO,
    RetrieveCompanyInputDTO, UpdateCompanyInputDTO
)
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Company, User
from src.infrastructure.databases import DAOInterface


class CompanyDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de empresa
    """

    async def create(
        self,
        dto: CreateCompanyInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Company:
        """
        Cria a empresa passando como argumento os dados da mesma.
        """

        company = Company(**dto.to_dict(exclude=["user_id", "employees"]))

        with DBConnectionHandler.connect(close_session) as database:
            try:
                # Inserir o owner
                # Inserir os employess

                database.session.add(company)
                if commit:
                    database.session.commit()
                    logging.info("Empresa inseridada no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a empresa: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return company

    async def list(self, dto: ListCompaniesInputDTO, close_session: bool = True) -> list[Company]:
        """
        Pega uma lista de empresas e filtra elas.
        """

        companies: list[Company] = []
        with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Company)

            if dto:
                if dto.employees:
                    statement: Select = statement \
                        .join(User, Company.owner_id == User.id) \
                        .where(User.email.in_(dto.employees))

                if dto.user_id:
                    statement: Select = statement.where(Company.owner_id == dto.user_id)

                if dto.name:
                    statement: Select = statement.where(Company.name.like(f"%{dto.name}%"))

                if dto.cnpj:
                    statement: Select = statement.where(Company.cnpj == dto.cnpj)

            try:
                companies = database.session.scalars(statement=statement).all()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao listar as empresas: {e}")
                database.close_session(True)
                raise e

        return companies

    async def get_by_id(self, _id: int, close_session: bool = True) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo _id
        """

        company: Company = None
        with DBConnectionHandler.connect(close_session) as database:
            try:
                company = database.session.get(Company, _id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da empresa: {e}")
                database.close_session(True)
                raise e

        return company

    async def retrieve(self, dto: RetrieveCompanyInputDTO, close_session: bool = True) -> Optional[Company]:
        """
        Pega os dados de uma empresa por outros atributos
        """

        company: Company = None
        with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Company).where(Company.cnpj == dto.cnpj)

            try:
                company = database.session.scalars(statement).one()
            except NoResultFound as e:
                logging.warning(f"Empresa com cnpj {dto.cnpj} não encontrada: {e}")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da empresa: {e}")
                database.close_session()
                raise e

        return company

    async def update(
        self,
        _id: int,
        dto: UpdateCompanyInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo _id e atualiza
        """

        company: Company = None
        with DBConnectionHandler.connect(close_session) as database:
            statement = select(Company).where(Company.id == _id)

            try:
                company = database.session.scalars(statement).one()
                if dto.cnpj:
                    company.cnpj = dto.cnpj

                if dto.name:
                    company.name = dto.name

                if dto.fantasy_name:
                    company.fantasy_name = dto.fantasy_name

                if dto.employees:
                    print("Desenvolver")

                if commit:
                    database.session.commit()
                    logging.info("Empresa atualizada no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar a empresa: {e}")
                database.session.rollback()
                database.close_session()
                raise e

        return company

    async def delete(
        self,
        cnpj: str,
        commit: bool = True,
        close_session: bool = True) -> None:
        """
        Pega os dados de uma empresa pelo _id e deleta ela
        """

        with DBConnectionHandler.connect(close_session) as database:
            try:
                company = database.session.get(Company, cnpj)
                if not company:
                    raise ValueError(f"Empresa com o cnpj {cnpj} não encontrado.")

                database.session.delete(company)
                if commit:
                    database.session.commit()
                    logging.info("Empresa deletada do banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao deletar a empresa: {e}")
                database.session.rollback()
                database.close_session()
                raise e

    async def count(self, close_session: bool = True) -> int:
        """
        Pega a quantidade de empresas registradas no banco.
        """

        qtd: int = 0
        with DBConnectionHandler.connect(close_session) as database:
            try:
                qtd = database.session.query(Company).count()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao realizar a contagem de empresas: {e}")
                database.close_session()
                raise e

        return qtd
