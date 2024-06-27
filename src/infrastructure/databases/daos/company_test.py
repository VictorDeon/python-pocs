import pytest
from src.adapters.dtos import (
    CreateUserInputDTO, CreateProfileInputDTO,
    CreateCompanyInputDTO, ListCompaniesInputDTO,
    UpdateCompanyInputDTO
)
from .user import UserDAO
from .company import CompanyDAO


async def test_create_company_dao():
    """
    Testa a criação de uma empresa pelo DAO.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=dto, close_session=False)

    try:
        assert company.cnpj == dto.cnpj
        assert company.name == dto.name
        assert company.fantasy_name == dto.fantasy_name
        assert company.owner_id == user01.id
        assert company.owner is not None
    finally:
        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)


async def test_list_companies_dao():
    """
    Listando as empresas.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto01 = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company01 = await dao.create(dto=company_dto01, close_session=False)

    company_dto02 = CreateCompanyInputDTO(
        cnpj="22222222222222",
        name="Empresa 02 LTDA",
        fantasy_name="Empresa 02",
        owner_id=user02.id
    )
    company02 = await dao.create(dto=company_dto02, close_session=False)

    dto = ListCompaniesInputDTO()
    companies = await dao.list(dto=dto, close_session=False)

    try:
        assert len(companies) == await dao.count()
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id
        assert companies[1].cnpj == company02.cnpj
        assert companies[1].name == company02.name
        assert companies[1].fantasy_name == company02.fantasy_name
        assert companies[1].owner_id == user02.id
    finally:
        await user_dao.delete(_id=user01.id, commit=False, close_session=False)
        await user_dao.delete(_id=user02.id, commit=False, close_session=False)
        await user_dao.delete(_id=user03.id, commit=True)


async def test_list_companies_by_owner_id_dao():
    """
    Listando as empresas com filtro de owner id.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto01 = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company01 = await dao.create(dto=company_dto01, close_session=False)

    company_dto02 = CreateCompanyInputDTO(
        cnpj="22222222222222",
        name="Empresa 02 LTDA",
        fantasy_name="Empresa 02",
        owner_id=user02.id
    )
    await dao.create(dto=company_dto02, close_session=False)

    dto = ListCompaniesInputDTO(owner_id=user01.id)
    companies = await dao.list(dto=dto, close_session=False)

    try:
        assert len(companies) == 1
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id
    finally:
        await user_dao.delete(_id=user01.id, commit=False, close_session=False)
        await user_dao.delete(_id=user02.id, commit=False, close_session=False)
        await user_dao.delete(_id=user03.id, commit=True)


async def test_list_companies_by_name_dao():
    """
    Listando as empresas pelo seu nome.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto01 = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company01 = await dao.create(dto=company_dto01, close_session=False)

    company_dto02 = CreateCompanyInputDTO(
        cnpj="22222222222222",
        name="Empresa 02 LTDA",
        fantasy_name="Empresa 02",
        owner_id=user02.id
    )
    company02 = await dao.create(dto=company_dto02, close_session=False)

    dto = ListCompaniesInputDTO(name="LTDA")
    companies = await dao.list(dto=dto, close_session=False)

    try:
        assert len(companies) == await dao.count()
        assert companies[0].cnpj == company01.cnpj
        assert companies[0].name == company01.name
        assert companies[0].fantasy_name == company01.fantasy_name
        assert companies[0].owner_id == user01.id
        assert companies[1].cnpj == company02.cnpj
        assert companies[1].name == company02.name
        assert companies[1].fantasy_name == company02.fantasy_name
        assert companies[1].owner_id == user02.id
    finally:
        await user_dao.delete(_id=user01.id, commit=False, close_session=False)
        await user_dao.delete(_id=user02.id, commit=False, close_session=False)
        await user_dao.delete(_id=user03.id, commit=True)


async def test_get_by_cnpj_company_dao():
    """
    Testa a busca de uma empresa pelo cnpj.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=dto, close_session=False)

    searched_company = await dao.get_by_cnpj(cnpj=company.cnpj)

    try:
        assert company.cnpj == searched_company.cnpj
        assert company.name == searched_company.name
        assert company.fantasy_name == searched_company.fantasy_name
        assert company.owner_id == searched_company.owner_id
        assert company.owner == searched_company.owner
    finally:
        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)


async def test_update_name_company_dao():
    """
    Testa a atualização do nome da empresa.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=company_dto, close_session=False)

    dto = UpdateCompanyInputDTO(name="Empresa 01 atualizada LTDA")
    updated_company = await dao.update(cnpj=company.cnpj, dto=dto, close_session=False)

    try:
        assert updated_company.cnpj == company.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == company.fantasy_name
        assert updated_company.owner_id == company.owner_id
        assert updated_company.owner == company.owner
    finally:
        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)


async def test_update_cnpj_company_dao():
    """
    Testa a atualização do nome e cnpj da empresa.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=company_dto, close_session=False)

    dto = UpdateCompanyInputDTO(
        name="Empresa 01 atualizada LTDA",
        cnpj="22222222222222"
    )
    updated_company = await dao.update(cnpj=company.cnpj, dto=dto, close_session=False)

    try:
        assert updated_company.cnpj == dto.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == company.fantasy_name
        assert updated_company.owner_id == company.owner_id
        assert updated_company.owner == company.owner
    finally:
        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)


async def test_update_fantasy_name_company_dao():
    """
    Testa a atualização do nome, nome fantasia e cnpj da empresa.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)

    dao = CompanyDAO()
    company_dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=company_dto, close_session=False)

    dto = UpdateCompanyInputDTO(
        name="Empresa 01 atualizada LTDA",
        fantasy_name="Empresa 01 atualizada"
    )
    updated_company = await dao.update(cnpj=company.cnpj, dto=dto, close_session=False)

    try:
        assert updated_company.cnpj == company.cnpj
        assert updated_company.name == dto.name
        assert updated_company.fantasy_name == dto.fantasy_name
        assert updated_company.owner_id == company.owner_id
        assert updated_company.owner == company.owner
    finally:
        await user_dao.delete(_id=user01.id)
        await user_dao.delete(_id=user02.id)
        await user_dao.delete(_id=user03.id)


async def test_delete_company_dao():
    """
    Testa a deleção da empresa sem deletar o usuário vinculado a ela como dono e nem
    os usuários funcionários.
    """

    user_dao = UserDAO()
    user_dto01 = CreateUserInputDTO(
        name="Fulano 01",
        email="fulano01@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956")
    )
    user01 = await user_dao.create(dto=user_dto01, close_session=False)
    assert user01 is not None

    user_dto02 = CreateUserInputDTO(
        name="Fulano 02",
        email="fulano02@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user02 = await user_dao.create(dto=user_dto02, close_session=False)
    assert user02 is not None

    user_dto03 = CreateUserInputDTO(
        name="Fulano 03",
        email="fulano03@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    user03 = await user_dao.create(dto=user_dto03, close_session=False)
    assert user03 is not None

    dao = CompanyDAO()
    dto = CreateCompanyInputDTO(
        cnpj="11111111111111",
        name="Empresa 01 LTDA",
        fantasy_name="Empresa 01",
        owner_id=user01.id
    )
    company = await dao.create(dto=dto, close_session=False)

    await dao.delete(cnpj=company.cnpj, close_session=False)

    company = await dao.get_by_cnpj(cnpj=company.cnpj, close_session=False)
    assert company is None

    user01 = await user_dao.get_by_id(_id=user01.id, close_session=False)
    assert user01 is not None

    user02 = await user_dao.get_by_id(_id=user02.id, close_session=False)
    assert user02 is not None

    user03 = await user_dao.get_by_id(_id=user03.id, close_session=False)
    assert user03 is not None

    await user_dao.delete(_id=user01.id)
    await user_dao.delete(_id=user02.id)
    await user_dao.delete(_id=user03.id)
