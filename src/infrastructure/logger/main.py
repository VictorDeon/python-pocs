import logging.handlers
import os
import logging
from datetime import datetime
from pytz import timezone


class ProjectLoggerSingleton:
    """
    Log do projeto
    """

    __instance = None

    def __init__(self):
        """
        Construtor.
        """

        if self.__instance is not None:
            raise TypeError("A instancia do log já existe. Utilize o método get_logger.")

        self.__logger = logging.getLogger('python-poc')

        # Configurar o level do log
        self.level = os.environ.get("LOG_LEVEL")
        self.__logger.setLevel(level=self.__get_log_level())

        # Formatar a saída de dados do log
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s File %(pathname)s, line %(lineno)d, in %(funcName)s [%(msecs)dms]:\n\t> '%(message)s'",
            datefmt="%d/%m/%Y %H:%M:%S"
        )
        sp = timezone("America/Sao_Paulo")
        formatter.converter = lambda *args: datetime.now(tz=sp).timetuple()

        # Inserir o handler do console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)
        self.__logger.propagate = False

        # Inserir o handler de arquivo rotativo, ou seja, se chegar a 2MB o arquivo, cria
        # um novo com o nome debug.log.[1..5]
        file_handler = logging.handlers.RotatingFileHandler(
            filename="assets/profiles/debug.log",
            mode="a",
            maxBytes=2 * (1024 * 1024),
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.__logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls):
        """
        Pega a instância do log do projeto.
        """

        if not cls.__instance:
            cls.__instance = ProjectLoggerSingleton()

        return cls.__instance.__logger

    def __get_log_level(self) -> int:
        """
        Instancia o level do log.
        """

        if self.level == "INFO":
            lvl = logging.INFO
        elif self.level == "ERROR":
            lvl = logging.ERROR
        elif self.level == "CRITICAL":
            lvl = logging.CRITICAL
        elif self.level == "WARNING":
            lvl = logging.WARNING
        else:
            lvl = logging.DEBUG

        return lvl
