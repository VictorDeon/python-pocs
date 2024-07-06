from typing import Optional
from datetime import datetime
from sqlalchemy import (
    insert, Insert,
    delete, Delete,
    update, Update
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from src.shared.exceptions import GenericException
from src.crud.permissions.dtos import RetrievePermissionInputDTO
from src.crud.companies.models import Company
from src.crud.permissions.repositories import RetrievePermissionDAO
from src.crud.groups.repositories import RetrieveGroupDAO
from src.crud.companies.repositories import RetrieveCompanyDAO
from ..models import User, UsersVsGroups, UsersVsPermissions
from ..dtos import UpdateUserInputDTO
from .profile import ProfileDAO


class UpdateUserRepository:
    """
    Repositorio de manipulação da entidade de usuários
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, dto: UpdateUserInputDTO, commit: bool = True) -> Optional[User]:
        """
        Pega os dados de um usuário pelo _id e atualiza
        """

        try:
            if dto.work_company_cnpj:
                company_dao = RetrieveCompanyDAO(session=self.session)
                company: Company = await company_dao.retrieve(cnpj=dto.work_company_cnpj)
                if not company:
                    raise GenericException(f"Empresa com cnpj {dto.work_company_cnpj} não encontrado.")

            statement: Update = update(User).values(
                name=dto.name,
                updated_at=datetime.now(),
                work_company_cnpj=dto.work_company_cnpj
            ).where(User.id == _id).returning(User)

            user: User = await self.session.scalar(statement)
            if not user:
                raise GenericException(f"Usuário com id {_id} não encontrado.")

            if dto.profile:
                profile_dao = ProfileDAO(session=self.session)
                await profile_dao.update(
                    user_id=user.id,
                    dto=dto.profile
                )

            if dto.permissions is not None:
                permission_dao = RetrievePermissionDAO(session=self.session)
                statement: Delete = delete(UsersVsPermissions).where(UsersVsPermissions.user_id == user.id)
                await self.session.execute(statement)

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

            if dto.groups is not None:
                group_dao = RetrieveGroupDAO(session=self.session)
                statement: Delete = delete(UsersVsGroups).where(UsersVsGroups.user_id == user.id)
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
                self.logger.info("Usuário atualizado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao atualizar o usuário: {e}")
            await self.session.rollback()
            raise e

        return user
