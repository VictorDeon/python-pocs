# flake8: noqa
# pylint: disable=wrong-import-position
from fastapi import APIRouter
router = APIRouter()
from .not_blocked_requests import *
from .pdf_generator import *
from .pdf_reader import *
from .list_pokemons import *
from .find_pokemon import *
