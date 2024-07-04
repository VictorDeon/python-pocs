from fastapi import Query
from src.application.api.routes import router
from src.adapters.controllers import ProfileRequestController
from src.adapters.dtos import ProfileRequestsOutputDTO


@router.get(
    "/profile-requests",
    tags=["Requests"],
    response_model=ProfileRequestsOutputDTO,
    summary="Realiza requisições de perfil."
)
async def profile_requests(
    qtd: int = Query(..., description="Quantidade de vezes a ser executada o comando."),
    sort: str = Query("tottime", description="Ordenar pelo parâmetro listado.")):
    """
    Executa e calcula o desempenho e consume de memória com o cprofile.
    ## Linha de comando:

    ### Gerar o cprofile do seu código
    * python -m cProfile -o output.stats uvicorn ...
    * python -m pstats output.stats
        - stats N
        - sort <params>
        - quit

    ### Com o output.stats gere uma imagem com a arvore de chamadas
    * pip install gprof2dot
    * gprof2dot -f pstats output.stats | dot -T png -o output.png

    ### Verifique sua aplicação em tempo real
    * pip install py-spy
    * py-spy top -- python uvicorn ...

    ### profile com corotines
    * pip install pyinstrument
    * pyinstrument uvicorn ...

    ## Parâmetros:
    * **ncalls**: Números de chamadas do método
    * **tottime**: Tempo total de execução do método sem as chamadas internas a outros métodos * ncalls
    * **percall**: Tempo total de execução do método sem as chamadas internas a outros métodos
    * **cumtime**: Tempo de espera que esse método teve com suas chamadas internas a outros métodos * ncalls
    * **percall**: Tempo de espera que esse método teve com suas chamadas internas a outros métodos
    * **filename**: Caminho do método
    """

    controller = ProfileRequestController()
    return await controller.execute(qtd, sort)
