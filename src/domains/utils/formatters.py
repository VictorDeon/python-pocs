import json
from decimal import Decimal
from datetime import datetime, date


class JsonFormatter(json.JSONEncoder):
    """
    Transforma alguns dados do python em json.
    """

    def default(self, o: json) -> json:
        """
        Valor padrão de formatação
        """

        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, (datetime, date)):
            return o.isoformat()
        elif isinstance(o, Exception):
            return str(o)
        else:
            return super().default(o)
