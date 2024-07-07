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
        Teste de carga no endpoint de poc de requisições.
        """

        print(f"[{datetime.now()}] Sou a requisição pela pagina web")
        print(f"Token: {self.token}")

        self.client.post("/users", json={
            "email": "fulano01@gmail.com",
            "groups": [
                226
            ],
            "name": "Fulano 01",
            "password": "Django1234",
            "permissions": [
                "permission_create",
                "permission_update"
            ],
            "profile": {
                "address": "Rua ABC bairro Ipanema N 244, Sorocaba, SP. CEP: 7059483",
                "phone": "61998283934"
            },
            "work_company_cnpj": "11111111111111"
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
