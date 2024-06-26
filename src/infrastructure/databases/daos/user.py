import logging
from sqlalchemy import Select, select
from src.adapters.dtos import (
    CreateUserInputDTO, RetrievePermissionInputDTO,
    RetrieveCompanyInputDTO, ListUserInputDTO
)
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import User
from src.infrastructure.databases import DAOInterface
from .permission import PermissionDAO
from .company import CompanyDAO
from .group import GroupDAO
from .profile import ProfileDAO


class UserDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de usuários
    """

    async def create(
        self,
        dto: CreateUserInputDTO,
        commit: bool = True,
        close_session: bool = True) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        user = User(
            name=dto.name,
            email=dto.email,
            password=dto.password
        )
        permission_dao = PermissionDAO()
        group_dao = GroupDAO()
        profile_dao = ProfileDAO()
        company_dao = CompanyDAO()

        with DBConnectionHandler.connect(close_session) as database:
            try:
                profile = await profile_dao.create(
                    dto=dto.profile,
                    close_session=False
                )
                user.profile_id = profile.id
                user.profile = profile

                if dto.work_company_cnpj:
                    work_company = await company_dao.retrieve(
                        dto=RetrieveCompanyInputDTO(cnpj=dto.work_company_cnpj),
                        close_session=False
                    )

                    if work_company:
                        user.work_company_cnpj = work_company.cnpj
                        user.work_company = work_company

                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code),
                        close_session=False
                    )
                    if permission:
                        user.permissions.append(permission)

                for group_id in dto.groups:
                    group = await group_dao.get_by_id(_id=group_id, close_session=False)
                    if group:
                        user.groups.append(group)

                database.session.add(user)
                if commit:
                    database.session.commit()
                    logging.info("Usuário inseridado no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return user

    async def list(self, dto: ListUserInputDTO, close_session: bool = True) -> list[User]:
        """
        Pega uma lista de objetos.
        """

        users: list[User] = []
        with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(User)

            if dto:
                if dto.name:
                    statement: Select = statement.where(User.name.like(f"%{dto.name}%"))

                if dto.email:
                    statement: Select = statement.where(User.email == dto.email)

            try:
                users = database.session.scalars(statement=statement).all()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao listar os usuários: {e}")
                database.close_session(True)
                raise e

        return users
