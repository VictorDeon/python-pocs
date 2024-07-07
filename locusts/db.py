from locust import HttpUser, SequentialTaskSet, task, between, events
from datetime import datetime


@events.test_start.add_listener
def script_start(*args, **kwargs):
    """
    Executado antes dos testes iniciarem.
    """

    print("Realizando algum login, conexão com banco ou arquivo de configuração.")
    print(args, kwargs)


@events.test_stop.add_listener
def script_end(*args, **kwargs):
    """
    Executado depois dos testes finalizarem
    """

    print("Fechando alguma conexão, logout ou armazenando algo em algum arquivo.")
    print(args, kwargs)


class DBTask(SequentialTaskSet):
    """
    Realiza a autenticação e a execução do endpoint de
    forma sequencial.
    TODO: Popular as permissões com um arquivo csv
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: str = None

    def on_start(self):
        """
        Realiza a autenticação.
        """

        print(f"[{datetime.now()}] Autenticando no sistema")
        self.token = "abcd1234"

    @task
    def poc_request(self):
        """
        Teste de carga no endpoint de CRUD de permissões.
        """

        print(f"[{datetime.now()}] Sou a requisição para criar uma permissão")
        print(f"Token: {self.token}")

        self.client.post("/permissions", json={
            "code": "permission_create",
            "name": "Permissão para criar permissões"
        }, headers={"accept": "application/json"})

    def on_stop(self):
        """
        Realiza a autenticação.
        """

        print(f"[{datetime.now()}] Sai do sistema")


class WebUserRequest(HttpUser):
    """
    Geração de teste de carga para performances com usuário da web.
    """

    wait_time = between(1, 5)
    weight = 1
    tasks = [DBTask]


class MobileUserRequest(HttpUser):
    """
    Geração de teste de carga para performances com usuários de aplicativos mobile.
    """

    wait_time = between(1, 2)
    weight = 3
    tasks = [DBTask]
