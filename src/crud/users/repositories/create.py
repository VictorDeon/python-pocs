from sqlalchemy import insert, Insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from src.shared.exceptions import GenericException
from src.crud.permissions.dtos import RetrievePermissionInputDTO
from ..models import User, UsersVsGroups, UsersVsPermissions
from ..dtos import CreateUserInputDTO
from src.crud.permissions.repositories import RetrievePermissionDAO
from src.crud.groups.repositories import RetrieveGroupDAO
from src.crud.companies.repositories import RetrieveCompanyDAO
from .profile import ProfileDAO


class CreateUserRepository:
    """
    Repositorio de manipulação da entidade de usuários
    """

    def __init__(self, session: AsyncSession):
        """
        Contrutor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, dto: CreateUserInputDTO, commit: bool = True) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        permission_dao = RetrievePermissionDAO(session=self.session)
        group_dao = RetrieveGroupDAO(session=self.session)
        profile_dao = ProfileDAO(session=self.session)
        company_dao = RetrieveCompanyDAO(session=self.session)

        try:
            if dto.work_company_cnpj:
                work_company = await company_dao.retrieve(cnpj=dto.work_company_cnpj)
                if not work_company:
                    raise GenericException(f"Empresa com cnpj {dto.work_company_cnpj} não encontrado.")

            statement: Insert = insert(User).values(
                name=dto.name,
                email=dto.email,
                password=dto.password,
                work_company_cnpj=dto.work_company_cnpj
            ).returning(User)
            user: User = await self.session.scalar(statement)

            await profile_dao.create(user_id=user.id, dto=dto.profile)

            for permission_code in dto.permissions:
                permission = await permission_dao.retrieve(
                    dto=RetrievePermissionInputDTO(code=permission_code)
                )
                if permission:
                    statement: Insert = insert(UsersVsPermissions).values(
                        user_id=user.id,
                        permission_id=permission.id
                    )
                    await self.session.execute(statement)

            for group_id in dto.groups:
                group = await group_dao.get_by_id(_id=group_id)
                if group:
                    statement: Insert = insert(UsersVsGroups).values(
                        user_id=user.id,
                        group_id=group.id
                    )
                    await self.session.execute(statement)

            if commit:
                await self.session.commit()
                self.logger.info("Usuário inseridado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao criar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user
