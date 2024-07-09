from locust import HttpUser, task, constant, events
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


class PocRequest(HttpUser):
    """
    Geração de teste de carga para performances com usuário da web.
    """

    wait_time = constant(0.5)

    @task
    def poc_request(self):
        """
        Teste de carga no endpoint de poc de requisições.
        """

        print(f"[{datetime.now()}] Sou a requisição pela pagina web")

        self.client.get("/poc-requests", headers={
            "accept": "application/json",
            "command": "DBSingletonConnectionPool"
        })
