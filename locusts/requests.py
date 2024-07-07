from locust import HttpUser, task, between
from datetime import datetime


class PocRequest(HttpUser):
    """
    Geração de teste de carga para performances com usuário da web.
    """

    wait_time = between(1, 5)

    @task
    def poc_request(self):
        """
        Teste de carga no endpoint de poc de requisições.
        """

        print(f"[{datetime.now()}] Sou a requisição pela pagina web")

        self.client.get("/poc-requests", headers={
            "accept": "application/json",
            "command": "HTTPxSingletonConnectionPool"
        })
