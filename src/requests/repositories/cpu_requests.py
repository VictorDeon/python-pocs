import math
import threading
import multiprocessing
import random
import queue
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

        logger.info("Iniciando o cálculo cpu-bound com")

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


class PocMultiThreadCPUBoundRequestRepository:
    """
    Testando o uso de multi threads em cpu bound
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadCPUBoundRequests"
        self.qtd_cores = multiprocessing.cpu_count()

    def computer(self, start: int, end: int) -> None:
        """
        Realiza o pode computacional.
        """

        logger.info("Iniciando o cálculo")

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
        logger.info(f"Iniciando a chamada {self.command} com {self.qtd_cores} core(s).")

        logger.info("Criando a threads e inserindo-as na pool de threads prontas para execução do processador.")
        threads: list[threading.Thread] = []
        for n in range(1, self.qtd_cores + 1):
            initial = 10_000_000 * (n - 1) / self.qtd_cores
            end = 10_000_000 * n / self.qtd_cores
            logger.info(f"Core {n} processando de {initial} até {end}")
            threads.append(
                threading.Thread(
                    name=f"cpu-bound-core-{n}",
                    daemon=True,
                    target=self.computer,
                    kwargs={"start": initial, "end": end}
                ),
            )

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

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


class PocMultiThreadWithLockRequestRepository:
    """
    Testando o uso de multi threads em cpu bound com lock para
    que as threads não utilizem recursos compatilhados ao mesmo tempo,
    por exemplo BackAccount.saldo ou self.qtd_inconsistent
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadWithLockRequests"
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


class PocMultiThreadWithQueueRequestRepository:
    """
    Realizando a comunicação entre threads que dependem uma das outras
    usando queue.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.command = "MultiThreadWithQueueRequests"

    def generate_data(self, queue: queue.Queue) -> None:
        """
        Gera os dados e insere na queue.
        """

        for i in range(1, 11):
            logger.info(f"Dado {i} gerado.")
            queue.put(i)

    def process_data(self, queue: queue.Queue) -> None:
        """
        Processa os dados recebidos.
        """

        while queue.qsize() > 0:
            value = queue.get()
            logger.info(f"Dado {value * 2} processado.")
            queue.task_done()

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        data_queue = queue.Queue()
        logger.info(f"Iniciando a chamada {self.command}")

        thread_generator = threading.Thread(target=self.generate_data, args=(data_queue,))
        thread_processor = threading.Thread(target=self.process_data, args=(data_queue,))

        thread_generator.start()
        thread_generator.join()

        thread_processor.start()
        thread_processor.join()

        end_time = time() - start_time
        logger.info(f"Requisição executada em {round(end_time, 2)} segundos")
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
