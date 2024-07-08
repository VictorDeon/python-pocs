import math
import threading
import random
from time import time, sleep
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


class PocCPUBoundRequestRepository:
    """
    Testando o uso de requisição cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "CPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info("Iniciando o cálculo cpu-bound")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        start = 1
        end = 10_000_000
        logger.info(f"Iniciando a chamada {self.command}")

        self.computer(start, end)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocSimplethreadCPUBoundRequestRepository:
    """
    Testando o uso de threads simples em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "SimpleThreadCPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info("Iniciando o cálculo cpu-bound")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a thread e inserindo na pool de threads prontas para execução do processador.")
        thread = threading.Thread(name="cpu-bound", target=self.computer, args=(1, 10_000_000))
        thread.start()

        logger.info("Processando outras coisas")
        sleep(5)
        logger.info(f"Aguardando até a {thread.name} ser executada e finalizada.")
        thread.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class BankAccount:
    """
    Conta bancária.
    """

    def __init__(self, saldo=0) -> None:
        """
        Construtor.
        """

        self.saldo = saldo

    def transfer(self, destination_account: "BankAccount", value: int) -> None:
        """
        Realiza a transferência entre as contas.
        """

        if self.saldo < value:
            return

        self.saldo -= value
        sleep(0.001)
        destination_account.saldo += value


class PocMultiplethreadCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadCPUBoundRequests"
        self.lock = threading.RLock()
        self.qtd_inconsistent = 0

    def create_bank_accounts(self) -> list[BankAccount]:
        """
        Cria 5 contas com saldo entre 5 mil e 10 mil reais.
        """

        return [
            BankAccount(saldo=random.randint(5_000, 10_000)),
            BankAccount(saldo=random.randint(5_000, 10_000)),
            BankAccount(saldo=random.randint(5_000, 10_000)),
            BankAccount(saldo=random.randint(5_000, 10_000)),
            BankAccount(saldo=random.randint(5_000, 10_000))
        ]

    def get_random_accounts(self, accounts: list[BankAccount]) -> tuple[BankAccount, BankAccount]:
        """
        Pega 2 contas randomicamente para realizar as
        transferências.
        """

        origin_account = random.choice(accounts)
        destination_account = random.choice(accounts)

        while origin_account == destination_account:
            destination_account = random.choice(accounts)

        return origin_account, destination_account

    def verify_bank_integrity(self, accounts: list[BankAccount], total: int) -> None:
        """
        Valida a integridade dos dados do banco se o saldo permanece
        o mesmo após as transferências.
        """

        with self.lock:
            current = sum(account.saldo for account in accounts)

        if current != total:
            logger.error(f"ERRO: Balanço bancário inconsistente. Atual R$ {current:.2f}, Total R$ {total:.2f}")
            with self.lock:
                self.qtd_inconsistent += 1
        else:
            logger.info(f"SUCESSO: Balanço bancário consistente. Atual R$ {current:.2f}, Total R$ {total:.2f}")

    def services(self, accounts: list[BankAccount], total: int) -> None:
        """
        Realiza as transferências.
        """

        for _ in range(1, 2_000):
            origin_account, destination_account = self.get_random_accounts(accounts)
            value = random.randint(1, 100)
            with self.lock:
                origin_account.transfer(destination_account, value)

            self.verify_bank_integrity(accounts, total)

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste evitando race conditions entre multiplas threads
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        bank_accounts = self.create_bank_accounts()
        with self.lock:
            total = sum(account.saldo for account in bank_accounts)

        logger.info(f"O saldo total das contas é de {total:.2f}")
        logger.info("Iniciando transferências...")

        tasks = [
            threading.Thread(target=self.services, args=(bank_accounts, total)),
            threading.Thread(target=self.services, args=(bank_accounts, total)),
            threading.Thread(target=self.services, args=(bank_accounts, total)),
            threading.Thread(target=self.services, args=(bank_accounts, total)),
            threading.Thread(target=self.services, args=(bank_accounts, total))
        ]
        [task.start() for task in tasks]
        [task.join() for task in tasks]

        logger.info(f"Transferências completadas com sucesso com {self.qtd_inconsistent} inconsistências.")
        self.verify_bank_integrity(bank_accounts, total)

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")


class PocMultiThreadBackgroundCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound em background
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadBackgroundCPUBoundRequests"

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info("Iniciando o cálculo cpu-bound")

        i = start
        factor = 1000 * 1000
        while i < end:
            i += 1
            math.sqrt((i - factor) * (i - factor))

        logger.info("Finalizando calculo")

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command}")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        self.threads = [
            threading.Thread(name="cpu-bound01", daemon=True, target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound02", daemon=True, target=self.computer, args=(1, 10_000_000)),
            threading.Thread(name="cpu-bound03", daemon=True, target=self.computer, args=(1, 10_000_000))
        ]
        [thread.start() for thread in self.threads]

        logger.info("Processando outras coisas")
        sleep(5)
        logger.info("Aguardando até as threads serem executadas e finalizadas.")

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
