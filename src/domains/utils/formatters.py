import json
from decimal import Decimal
from datetime import datetime, date
from typing import Any


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


def paginated(objs: list[Any], offset: int = None, limit: int = None) -> list[Any]:
    """
    Realiza a paginação nos objetos.
    """

    if offset and limit:
        return objs[offset:limit + offset]
    elif offset:
        return objs[offset:]
    elif limit:
        return objs[:limit]
    else:
        return objs

