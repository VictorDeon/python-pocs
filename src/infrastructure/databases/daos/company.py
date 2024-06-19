import logging
from src.domains.entities import Company, User
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import (
    Company as CompanyModel,
    User as UserModel
)
from src.infrastructure.databases.interfaces import UserDAOInterface


class CompanyDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade de empresa
    """

    async def create(
        self,
        cnpj: str,
        name: str,
        fantasy_name: str,
        owner: UserModel,
        employees: list[UserModel]) -> Company:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """


        company = CompanyModel(
            cnpj=cnpj,
            name=name,
            fantasy_name=fantasy_name,
            owner=owner,
            employees=employees
        )

        with DBConnectionHandler() as database:
            try:
                database.session.add(company)
                database.session.commit()
                logging.info(f"Empresa {company.cnpj} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a empresa: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return Company(
            cnpj=company.cnpj,
            name=company.name,
            fantasy_name=company.fantasy_name,
            owner=User(**company.owner),
            employees=[
                User(**user) for user in company.employees
            ]
        )
