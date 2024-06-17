import json
from decimal import Decimal
from datetime import datetime, date


class JsonFormatter(json.JSONEncoder):
    """
    Transforma alguns dados do python em json.
    """

    def default(self, obj: json.Any) -> json.Any:
        """
        Valor padrão de formatação
        """

        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Exception):
            return str(obj)
        else:
            return super().default(obj)
