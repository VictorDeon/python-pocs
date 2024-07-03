from src.adapters.dtos import (
    CreateUserInputDTO, CreateProfileInputDTO,
    CreateCompanyInputDTO, ListCompaniesInputDTO,
    UpdateCompanyInputDTO
)
from src.infrastructure.databases import DBConnectionHandler
from .user import UserDAO
from .company import CompanyDAO


async def test_create_company_dao():
    """
    Testa a criação de uma empresa pelo DAO.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=dto)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            work_company_cnpj=company.cnpj,
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto02)

        assert company.cnpj == dto.cnpj
        assert company.name == dto.name
        assert company.fantasy_name == dto.fantasy_name
        assert company.owner_id == user01.id


async def test_list_companies_dao():
    """
    Listando as empresas.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        user02 = await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto01 = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company01 = await dao.create(dto=company_dto01)

        company_dto02 = CreateCompanyInputDTO(
            cnpj="22222222222222",
            name="Empresa 02 LTDA",
            fantasy_name="Empresa 02",
            owner_id=user02.id
        )
        company02 = await dao.create(dto=company_dto02)

        dto = ListCompaniesInputDTO()
        companies = await dao.list(dto=dto)

        assert len(companies) == await dao.count()
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id
        assert companies[1].cnpj == company02.cnpj
        assert companies[1].name == company02.name
        assert companies[1].fantasy_name == company02.fantasy_name
        assert companies[1].owner_id == user02.id


async def test_list_companies_by_owner_id_dao():
    """
    Listando as empresas com filtro de owner id.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        user02 = await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto01 = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company01 = await dao.create(dto=company_dto01)

        company_dto02 = CreateCompanyInputDTO(
            cnpj="22222222222222",
            name="Empresa 02 LTDA",
            fantasy_name="Empresa 02",
            owner_id=user02.id
        )
        await dao.create(dto=company_dto02)

        dto = ListCompaniesInputDTO(owner_id=user01.id)
        companies = await dao.list(dto=dto)

        assert len(companies) == 1
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id


async def test_list_companies_by_name_dao():
    """
    Listando as empresas pelo seu nome.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        user02 = await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto01 = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company01 = await dao.create(dto=company_dto01)

        company_dto02 = CreateCompanyInputDTO(
            cnpj="22222222222222",
            name="Empresa 02 LTDA",
            fantasy_name="Empresa 02",
            owner_id=user02.id
        )
        company02 = await dao.create(dto=company_dto02)

        dto = ListCompaniesInputDTO(name="LTDA")
        companies = await dao.list(dto=dto)

        assert len(companies) == await dao.count()
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id
        assert companies[1].cnpj == company02.cnpj
        assert companies[1].name == company02.name
        assert companies[1].fantasy_name == company02.fantasy_name
        assert companies[1].owner_id == user02.id


async def test_get_by_cnpj_company_dao():
    """
    Testa a busca de uma empresa pelo cnpj.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        dao = CompanyDAO(session=session)
        dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=dto)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            work_company_cnpj=company.cnpj,
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            work_company_cnpj=company.cnpj,
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        searched_company = await dao.retrieve(cnpj=company.cnpj)

        assert company.cnpj == searched_company.cnpj
        assert company.name == searched_company.name
        assert company.fantasy_name == searched_company.fantasy_name
        assert company.owner_id == searched_company.owner_id


async def test_update_name_company_dao():
    """
    Testa a atualização do nome da empresa.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=company_dto)

        dto = UpdateCompanyInputDTO(
            cnpj=company.cnpj,
            name="Empresa 01 atualizada LTDA"
        )
        updated_company = await dao.update(cnpj=company.cnpj, dto=dto)

        assert updated_company.cnpj == company.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == company.fantasy_name
        assert updated_company.owner_id == company.owner_id


async def test_update_cnpj_company_dao():
    """
    Testa a atualização do nome e cnpj da empresa.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=company_dto)

        dto = UpdateCompanyInputDTO(
            name="Empresa 01 atualizada LTDA",
            cnpj="22222222222222"
        )
        updated_company = await dao.update(cnpj=company.cnpj, dto=dto)

        assert updated_company.cnpj == dto.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == company.fantasy_name
        assert updated_company.owner_id == company.owner_id


async def test_update_fantasy_name_company_dao():
    """
    Testa a atualização do nome, nome fantasia e cnpj da empresa.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto02)

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        await user_dao.create(dto=user_dto03)

        dao = CompanyDAO(session=session)
        company_dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=company_dto)

        dto = UpdateCompanyInputDTO(
            name="Empresa 01 atualizada LTDA",
            cnpj=company.cnpj,
            fantasy_name="Empresa 01 atualizada"
        )
        updated_company = await dao.update(cnpj=company.cnpj, dto=dto)

        assert updated_company.cnpj == company.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == dto.fantasy_name
        assert updated_company.owner_id == company.owner_id


async def test_delete_company_dao():
    """
    Testa a deleção da empresa sem deletar o usuário vinculado a ela como dono e nem
    os usuários funcionários.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        user_dto01 = CreateUserInputDTO(
            name="Fulano 01",
            email="fulano01@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956")
        )
        user01 = await user_dao.create(dto=user_dto01)
        assert user01 is not None

        user_dto02 = CreateUserInputDTO(
            name="Fulano 02",
            email="fulano02@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        user02 = await user_dao.create(dto=user_dto02)
        assert user02 is not None

        user_dto03 = CreateUserInputDTO(
            name="Fulano 03",
            email="fulano03@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        user03 = await user_dao.create(dto=user_dto03)
        assert user03 is not None

        dao = CompanyDAO(session=session)
        dto = CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=user01.id
        )
        company = await dao.create(dto=dto)

        await dao.delete(cnpj=company.cnpj)

        company = await dao.retrieve(cnpj=company.cnpj)
        assert company is None

        user01 = await user_dao.get_by_id(_id=user01.id)
        assert user01 is not None

        user02 = await user_dao.get_by_id(_id=user02.id)
        assert user02 is not None

        user03 = await user_dao.get_by_id(_id=user03.id)
        assert user03 is not None

        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)
