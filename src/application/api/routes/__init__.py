# flake8: noqa
# pylint: disable=wrong-import-position
from fastapi import APIRouter
router = APIRouter()
from .blocked_requests import *
from .pdf_generator import *
from .pdf_reader import *
from .list_pokemons import *
from .find_pokemon import *
from .find_user import *
from .list_permissions import *
from .create_permission import *
from .retrieve_permission import *
from .update_permission import *
from .delete_permissions import *
