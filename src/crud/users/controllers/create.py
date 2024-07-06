from fastapi import status
from src.routes import router
from src.infrastructure.databases import DBConnectionHandler
from ..presenters import CreateUserPresenter
from ..dtos import CreateUserInputDTO, CreateUserOutputDTO
from ..repositories import CreateUserRepository


@router.post(
    "/users",
    tags=["Banco de Dados"],
    response_model=CreateUserOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um usuário."
)
async def create_user(data: CreateUserInputDTO):
    """
    Cria um usuário.
    """

    async with DBConnectionHandler() as session:
        repository = CreateUserRepository(session=session)
        output = CreateUserPresenter(session=session)
        model = await repository.execute(dto=data)
        return await output.present(model)
