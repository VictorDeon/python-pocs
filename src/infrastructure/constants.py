import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
POKEAPI_URL = os.getenv("POKEAPI_URL", "https://pokeapi.co/api/v2")
