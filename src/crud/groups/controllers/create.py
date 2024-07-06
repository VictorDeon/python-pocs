from fastapi import status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import CreateGroupInputDTO, CreateGroupOutputDTO
from ..repositories import CreateGroupDAO
from ..presenters import CreateGroupPresenter


@router.post(
    "/groups",
    tags=["CRUDs"],
    response_model=CreateGroupOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um grupo."
)
async def create_group(data: CreateGroupInputDTO):
    """
    Cria um grupo de usuários.
    """

    async with DBConnectionHandler() as session:
        repository = CreateGroupDAO(session=session)
        output = CreateGroupPresenter(session=session)
        model = await repository.execute(dto=data)
        return await output.present(model)
