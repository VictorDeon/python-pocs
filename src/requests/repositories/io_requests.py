from time import time
import asyncio
import os
import aiohttp
import httpx
from src.engines.logger import ProjectLoggerSingleton
from src.engines.constants import POKEAPI_URL
from src.engines.clients import HTTPxClient, HTTPxSingleton, AIOHTTPClient, AIOHTTPSingleton
from ..dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocHTTPxConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with httpx.AsyncClient() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20')
            ]
            responses: list[httpx.Response] = await asyncio.gather(*tasks)
            for response in responses:
                r1 = response.json()
                results += r1['results']

            logger.info(f"Quantidade retornada requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocHTTPxCustomConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx customizado.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxCustomConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with HTTPxClient() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20')
            ]
            responses: list[dict] = await asyncio.gather(*tasks)
            for response in responses:
                results += response['results']

            logger.info(f"Quantidade retornada da requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocHTTPxSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx com singleton.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxSingletonConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        client = await HTTPxSingleton.get_instance()

        start_time = time()
        results = []
        logger.info(f"Iniciando a chamada {self.command}")
        tasks = [
            client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
            client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
            client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20')
        ]
        responses: list[dict] = await asyncio.gather(*tasks)
        for response in responses:
            results += response['results']

        logger.info(f"Quantidade retornada da requisição: {len(results)}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocHTTPxSingletonSemaphoreConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do httpx com singleton e semaforo.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "HTTPxSingletonSemaphoreConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        client = await HTTPxSingleton.get_instance()
        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        async with asyncio.Semaphore(int(os.environ.get("SEMAPHORE", 1))):
            results = []
            tasks = [
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                client.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20')
            ]
            responses: list[dict] = await asyncio.gather(*tasks)
            for response in responses:
                results += response['results']

            logger.info(f"Quantidade retornada da requisição: {len(results)}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocAIOHTTPConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do iohttp.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPConnectionPool"

    async def make_request(self, session: aiohttp.ClientSession, limit: int = 10, offset: int = 0) -> list[dict]:
        """
        Realiza a requisição.
        """

        async with session.get(f'{POKEAPI_URL}/pokemon?limit={limit}&offset={offset}') as response:
            r1 = await response.json()
            return r1['results']

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with aiohttp.ClientSession() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                self.make_request(session, 10, 0),
                self.make_request(session, 10, 10),
                self.make_request(session, 10, 20),
            ]
            responses: list[list[dict]] = await asyncio.gather(*tasks)
            for response in responses:
                results += response

            logger.info(f"Quantidade retornada requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocAIOHTTPCustomConnectionPoolRepository:
    """
    Testando o uso do pool de conexões do iohttp customizado.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPCustomConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        async with AIOHTTPClient() as session:
            logger.info("Abrindo conexão")
            results = []
            tasks = [
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
                session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20'),
            ]
            responses: list[dict] = await asyncio.gather(*tasks)
            for response in responses:
                results += response['results']

            logger.info(f"Quantidade retornada requisição: {len(results)}")

        logger.info("Fechando conexão")
        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocAIOHTTPSingletonConnectionPoolRepository:
    """
    Testando o uso do pool de conexões singleton do iohttp.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "AIOHTTPSingletonConnectionPool"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")
        session = await AIOHTTPSingleton.get_instance()

        results = []
        tasks = [
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=0'),
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=10'),
            session.get(f'{POKEAPI_URL}/pokemon?limit=10&offset=20'),
        ]
        responses: list[dict] = await asyncio.gather(*tasks)
        for response in responses:
            results += response['results']

        logger.info(f"Quantidade retornada requisição: {len(results)}")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
