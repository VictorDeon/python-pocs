from multiprocessing import Process, current_process, Manager, Value, RLock as ProcessLock
from multiprocessing.synchronize import RLock
from time import time
import ctypes
import random
from src.engines.logger import ProjectLoggerSingleton
from ...dtos import PocRequestsOutputDTO

logger = ProjectLoggerSingleton.get_logger()


def modify_data(counter: ctypes.c_int, results: list[bool], objs: dict, lock: RLock) -> None:
    """
    Incrementa o contador e adicionar randomicamente um valor booleano na lista.
    """

    with lock:
        results.append(random.choice([True, False]))
        counter.value = counter.value + 1
        objs[f"{counter.value}^2"] = counter.value ** 2
        process_name = current_process().name
        logger.info(f"No processo [{process_name}] obtivemos: {counter.value}) {results[:]} e {objs}")


class PocMultiProcessShareMemoryRequestRepository:
    """
    Testando o uso do compartilhamento de memória entre processos.
    """

    def __init__(self) -> None:
        """
        Construtor.
        """

        self.command = "MultiProcessShareMemoryRequests"

    async def execute(self) -> PocRequestsOutputDTO:
        """
        Executa o teste
        """

        start_time = time()
        logger.info(f"Iniciando a chamada {self.command} no processo {current_process().name}")
        manager = Manager()
        lock = ProcessLock()

        counter = Value(ctypes.c_int, 0)
        results: list[bool] = manager.list()
        objs: dict = manager.dict()

        p1 = Process(target=modify_data, args=(counter, results, objs, lock))
        p2 = Process(target=modify_data, args=(counter, results, objs, lock))
        p3 = Process(target=modify_data, args=(counter, results, objs, lock))
        p4 = Process(target=modify_data, args=(counter, results, objs, lock))
        p5 = Process(target=modify_data, args=(counter, results, objs, lock))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

        end_time = time() - start_time
        return PocRequestsOutputDTO(result=f"Requisição executada em {round(end_time, 2)} segundos")
