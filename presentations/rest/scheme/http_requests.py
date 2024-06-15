class HttpRequest:
    """
    Define a entrada de dados de requisições externas
    """

    def __init__(
        self,
        url,
        body = None,
        query = None,
        path = None,
        headers = None,
        files = None,
        auth = None) -> None:
        """
        Construtor.
        """

        self.url = url
        self.body = body
        self.query = query
        self.path = path
        self.headers = headers
        self.files = files
        self.auth = auth
