"""
Essa pasta estará presente todos os serviços externos de infraestrutura como banco de dados,
mensageria, cache e etc.
"""

from .pubsub import PubsubSingleton

__all__ = ["PubsubSingleton"]
